"""Exercise the documented shell loop in a private tmux server; never connect over SSH."""

import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "skills/cmd-remote/references/session-protocol.md"
REQUIRED = ("tmux", "bash", "openssl", "perl")


def protocol_examples(document):
    """Named examples are the doc/test interface; headings and fence style may change."""
    matches = re.findall(
        r"<!-- protocol-example: ([\w-]+) -->\s*\n(`{3,}|~{3,})bash[^\S\n]*\n(.*?)\n\2[^\S\n]*(?=\n|$)",
        document, re.S,
    )
    examples = {}
    for name, _, body in matches:
        if name in examples:
            raise ValueError(f"Duplicate protocol example: {name}")
        examples[name] = body
    for name in ("sender", "reader"):
        if name not in examples:
            raise ValueError(f"Missing protocol example '{name}': expected its protocol-example comment followed by a Bash fence")
    return examples


class ProtocolDocumentationTests(unittest.TestCase):
    def test_fence_styles_and_extra_examples(self):
        document = REFERENCE.read_text()
        original = protocol_examples(document)
        modified = document.replace("~~~", "```") + (
            "\n<!-- protocol-example: extra-helper -->\n```bash\n: additional helper\n```\n"
        )
        examples = protocol_examples(modified)
        for name in ("sender", "reader"):
            self.assertEqual(examples[name], original[name])

    def test_missing_example_names_the_problem(self):
        document = REFERENCE.read_text().replace("protocol-example: sender", "protocol-example: other")
        with self.assertRaisesRegex(ValueError, "Missing protocol example 'sender'"):
            protocol_examples(document)


@unittest.skipUnless(all(shutil.which(tool) for tool in REQUIRED),
                     "Protocol tests require tmux, Bash, OpenSSL, and Perl")
class RemoteProtocolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cmd-remote-test-", dir="/tmp")
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.socket = str(self.work / "tmux.sock")
        self.addCleanup(self.stop_server)
        self.env = dict(os.environ)
        self.env.pop("TMUX", None)
        self.env.update(PS1="TEST> ", PS2="CONT> ", PROMPT_COMMAND="", HISTFILE="/dev/null")
        self.pane = self.tmux("new-session", "-d", "-P", "-F", "#{pane_id}",
                              "-s", "protocol", "-x", "200", "-y", "50",
                              "bash", "--noprofile", "--norc", "-i").strip()
        self.tmux("set-option", "-p", "-t", self.pane, "remain-on-exit", "on")
        self.log = self.work / "output.log"
        self.log.touch(mode=0o600)
        self.tmux("pipe-pane", "-O", "-t", self.pane, f"cat >> '{self.log}'")
        examples = protocol_examples(REFERENCE.read_text())
        self.helper = self.work / "protocol.sh"
        self.helper.write_text(
            'tmux() { command tmux -S "$CMD_REMOTE_SOCKET" "$@"; }\n'
            + examples["sender"] + "\n" + examples["reader"] + "\n"
        )
        self.env.update(CMD_REMOTE_SOCKET=self.socket, CMD_REMOTE_PANE=self.pane,
                        CMD_REMOTE_LOG=str(self.log))
        self.wait_for(lambda: "TEST>" in self.tmux("capture-pane", "-p", "-t", self.pane))

    def stop_server(self):
        subprocess.run(["tmux", "-S", self.socket, "kill-server"],
                       capture_output=True, timeout=5)

    def tmux(self, *args):
        result = subprocess.run(["tmux", "-S", self.socket, "-f", "/dev/null", *args],
                                env=self.env, text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        if args[0] == "new-session":
            self.assertTrue(result.stdout.strip().startswith("%"),
                            "tmux did not create a pane; check local socket permission: " + result.stderr)
        return result.stdout

    def shell(self, code, **extra):
        return subprocess.run(["bash", "--noprofile", "--norc", "-c",
                               'source "$1"; ' + code, "protocol", str(self.helper)],
                              env={**self.env, **extra}, cwd=self.work,
                              capture_output=True, text=True, timeout=5)

    def wait_for(self, check):
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            value = check()
            if value:
                return value
            time.sleep(0.025)
        self.fail("Timed out waiting for isolated test pane")

    def send(self, command):
        result = self.shell('cmd_remote_send || exit $?; '
                            'printf "%s %s\\n" "$CMD_REMOTE_NONCE" "$CMD_REMOTE_OFFSET"',
                            CMD=command)
        self.assertEqual(result.returncode, 0, result.stderr)
        nonce, offset = result.stdout.strip().split()
        self.env.update(CMD_REMOTE_NONCE=nonce, CMD_REMOTE_OFFSET=offset)

    def status(self):
        result = self.shell("cmd_remote_status")
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def run_command(self, command, expected_status=0):
        self.send(command)
        self.assertEqual(self.wait_for(self.status), str(expected_status))
        result = self.shell("cmd_remote_output")
        lines = result.stdout.splitlines()
        nonce = self.env["CMD_REMOTE_NONCE"]
        start = lines.index("__BEGIN_" + nonce)
        end = lines.index(f"__END_{nonce}:{expected_status}", start + 1)
        return "\n".join(lines[start + 1:end]).strip("\n")

    def test_output_boundaries_and_real_exit_status(self):
        for command, output, status in [
            ("printf 'no newline'", "no newline", 0),
            ("printf 'first\\nsecond\\n'", "first\nsecond", 0),
            (":", "", 0),
            ("false", "", 1),
            ("printf 'comment' # trailing comment", "comment", 0),
            ("false | true", "", 0),
            ("bash -o pipefail -c 'false | true'", "", 1),
            ("printf '\\033[31mred\\033[0m'", "red", 0),
            ("printf '\\033]0;first\\033\\\\visible\\033]0;second\\033\\\\'", "visible", 0),
            (": &", "", 0),
        ]:
            with self.subTest(command=command):
                actual = self.run_command(command, status)
                if command != ": &":  # interactive Bash may print its job ID
                    self.assertEqual(actual, output)

    def test_quotes_execute_remotely_and_shell_state_persists(self):
        self.run_command("cd /; export CMD_REMOTE_TEST_VALUE='state stays'")
        output = self.run_command('printf "%s|%s|%s" "$(pwd)" "$CMD_REMOTE_TEST_VALUE" "it\'s literal"')
        self.assertEqual(output, "/|state stays|it's literal")

    def test_stable_pane_when_user_selects_another(self):
        other = self.tmux("split-window", "-P", "-F", "#{pane_id}", "-t", self.pane,
                          "bash", "--noprofile", "--norc", "-i").strip()
        self.assertEqual(self.run_command("printf 'correct-pane'"), "correct-pane")
        self.assertNotIn("correct-pane", self.tmux("capture-pane", "-p", "-t", other))

    def test_pipe_flags_toggle_or_replace(self):
        self.tmux("pipe-pane", "-t", self.pane)  # close the task-owned setup pipe
        command = f"cat >> '{self.log}'"
        for flag, expected in (("-o", "1"), ("-o", "0"), ("-O", "1"), ("-O", "1")):
            with self.subTest(flag=flag, expected=expected):
                self.tmux("pipe-pane", flag, "-t", self.pane, command)
                self.assertEqual(self.tmux("display-message", "-p", "-t", self.pane,
                                           "#{pane_pipe}").strip(), expected)
        self.assertEqual(self.run_command("printf 'logging-restored'"), "logging-restored")

    def test_missing_completion_and_multiline_rejection(self):
        result = self.shell("cmd_remote_send", CMD="printf 'one'\nprintf 'two'")
        self.assertEqual(result.returncode, 2)
        self.send("sleep 0.4; printf 'finished'")
        self.assertEqual(self.status(), "")
        self.assertEqual(self.wait_for(self.status), "0")
        self.send("exit 7")
        self.wait_for(lambda: self.tmux("display-message", "-p", "-t", self.pane,
                                       "#{pane_dead}").strip() == "1")
        self.assertEqual(self.status(), "")


if __name__ == "__main__":
    unittest.main()

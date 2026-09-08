#!/bin/bash

# exit on error
set -e

# ANSI Color Codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Determine script directories
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC_DIR="$SCRIPT_DIR/skills"

show_help() {
  echo -e "${BOLD}Skill Uninstaller for Claude Code & Codex${NC}"
  echo "Easily remove installed repository skills locally or globally."
  echo
  echo -e "${BOLD}Usage:${NC}"
  echo "  ./uninstall.sh [options]"
  echo
  echo -e "${BOLD}Options:${NC}"
  echo "  -l, --local [PATH]    Uninstall locally from the specified project path (default: current directory)"
  echo "  -g, --global          Uninstall globally from your home directory"
  echo "  --dry-run            Show removals without writing files"
  echo "  -h, --help            Show this help message"
  echo
  echo -e "${BOLD}Examples:${NC}"
  echo "  ./uninstall.sh --local                   # Uninstall locally from current project"
  echo "  ./uninstall.sh --global                  # Uninstall globally"
  echo "  ./uninstall.sh --local ~/projects/my-app # Uninstall locally from a specific project"
  echo
}

LOCAL=false
LOCAL_PATH=""
GLOBAL=false
DRY_RUN=false

# Parse CLI arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    -l|--local)
      LOCAL=true
      if [[ -n "$2" && "$2" != -* ]]; then
        LOCAL_PATH="$2"
        shift
      else
        LOCAL_PATH="."
      fi
      ;;
    -g|--global)
      GLOBAL=true
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    --dry-run)
      DRY_RUN=true
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}" >&2
      show_help
      exit 1
      ;;
  esac
  shift
done

# If no target specified, run interactive mode
if [ "$LOCAL" = false ] && [ "$GLOBAL" = false ]; then
  echo -e "${BLUE}=== Skill Uninstaller for Claude Code & Codex ===${NC}"
  echo "Where would you like to uninstall the skills from?"
  echo "1) Uninstall locally from the current project"
  echo "2) Uninstall globally"
  echo "3) Uninstall both locally and globally"
  echo "4) Cancel"
  read -p "Select an option (1-4): " choice
  case $choice in
    1)
      LOCAL=true
      LOCAL_PATH="."
      ;;
    2)
      GLOBAL=true
      ;;
    3)
      LOCAL=true
      LOCAL_PATH="."
      GLOBAL=true
      ;;
    *)
      echo "Uninstallation cancelled."
      exit 0
      ;;
  esac
  echo
fi

# Verify source directory to get the list of skill names to remove
if [ ! -d "$SRC_DIR" ]; then
  echo -e "${RED}Error: Source skills directory not found at: $SRC_DIR${NC}" >&2
  echo "Using default list of skills to uninstall..."
  SKILLS=("spec-plan" "spec-apply" "spec-close" "spec-feedback" "spec-debug" "cmd-remote")
else
  # Find all skill folders
  SKILLS=()
  for dir in "$SRC_DIR"/*; do
    if [ -f "$dir/SKILL.md" ]; then
      SKILLS+=("$(basename "$dir")")
    fi
  done
fi


# Function to uninstall a skill and clean up empty parent directories
uninstall_skill() {
  local skill_name="$1"
  local target_parent_dir="$2"
  local dest_path="$target_parent_dir/$skill_name"

  if [ "$DRY_RUN" = true ]; then
    if [ -e "$dest_path" ] || [ -L "$dest_path" ]; then
      echo "Would remove: $dest_path"
    fi
    return
  fi

  if [ -e "$dest_path" ] || [ -L "$dest_path" ]; then
    if [ "$SRC_DIR/$skill_name" -ef "$dest_path" ] && [ ! -L "$dest_path" ]; then
      echo "Error: Destination is the source skill: $dest_path" >&2
      exit 1
    fi
    rm -rf "$dest_path"
    echo -e "  ${GREEN}✓${NC} Removed ${BOLD}$skill_name${NC} from $dest_path"
  fi

  # Clean up empty parent directories
  if [ -d "$target_parent_dir" ] && [ -z "$(ls -A "$target_parent_dir" 2>/dev/null)" ]; then
    rmdir "$target_parent_dir" 2>/dev/null || true
    
    # Check one level up (e.g. .claude/ if .claude/skills/ was empty)
    local grandpa_dir="$(dirname "$target_parent_dir")"
    if [ -d "$grandpa_dir" ] && [ -z "$(ls -A "$grandpa_dir" 2>/dev/null)" ]; then
      rmdir "$grandpa_dir" 2>/dev/null || true
    fi
  fi
}

# Run local uninstallation
if [ "$LOCAL" = true ]; then
  if [ -d "$LOCAL_PATH" ]; then
    ABS_LOCAL_PATH="$(cd "$LOCAL_PATH" && pwd)"
    echo -e "${BLUE}Uninstalling skills locally from: ${BOLD}$ABS_LOCAL_PATH${NC}..."
    
    # Claude Code local path
    CLAUDE_LOCAL="$ABS_LOCAL_PATH/.claude/skills"
    echo -e "${YELLOW}Uninstalling from Claude Code (.claude/skills/)...${NC}"
    for skill in "${SKILLS[@]}"; do
      uninstall_skill "$skill" "$CLAUDE_LOCAL"
    done
    
    # Codex local path
    CODEX_LOCAL="$ABS_LOCAL_PATH/.agents/skills"
    echo -e "${YELLOW}Uninstalling from Codex (.agents/skills/)...${NC}"
    for skill in "${SKILLS[@]}"; do
      uninstall_skill "$skill" "$CODEX_LOCAL"
    done
    echo
  else
    echo -e "${RED}Warning: Local path $LOCAL_PATH does not exist. Skipping local uninstall.${NC}"
  fi
fi

# Run global uninstallation
if [ "$GLOBAL" = true ]; then
  echo -e "${BLUE}Uninstalling skills globally...${NC}"
  
  # Claude Code global path
  CLAUDE_GLOBAL="$HOME/.claude/skills"
  echo -e "${YELLOW}Uninstalling from Claude Code (~/.claude/skills/)...${NC}"
  for skill in "${SKILLS[@]}"; do
    uninstall_skill "$skill" "$CLAUDE_GLOBAL"
  done
  
  # Codex global path
  CODEX_GLOBAL="$HOME/.agents/skills"
  echo -e "${YELLOW}Uninstalling from Codex (~/.agents/skills/)...${NC}"
  for skill in "${SKILLS[@]}"; do
    uninstall_skill "$skill" "$CODEX_GLOBAL"
  done
  echo
fi

if [ "$DRY_RUN" = true ]; then
  echo "Dry run complete; no files changed."
else
  echo -e "${GREEN}${BOLD}Uninstallation complete!${NC}"
fi

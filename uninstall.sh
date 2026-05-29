#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# AI Proposal Team — Claude Code Skill Uninstaller
# ============================================================

CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
AGENTS_DIR="${CLAUDE_DIR}/agents"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${YELLOW}AI Proposal Team — Uninstaller${NC}"
echo ""
echo "This will remove the following:"
echo ""

[ -d "$SKILLS_DIR/proposal" ] && echo "  → ${SKILLS_DIR}/proposal/"
for skill_dir in "$SKILLS_DIR"/proposal-*/; do
    [ -d "$skill_dir" ] && echo "  → ${skill_dir}"
done
for agent_file in "$AGENTS_DIR"/proposal-*.md; do
    [ -f "$agent_file" ] && echo "  → ${agent_file}"
done

echo ""
read -p "Are you sure you want to uninstall? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo ""

if [ -d "$SKILLS_DIR/proposal" ]; then
    rm -rf "$SKILLS_DIR/proposal"
    echo -e "${GREEN}✓ Removed main skill${NC}"
fi

for skill_dir in "$SKILLS_DIR"/proposal-*/; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        rm -rf "$skill_dir"
        echo -e "${GREEN}✓ Removed ${skill_name}${NC}"
    fi
done

for agent_file in "$AGENTS_DIR"/proposal-*.md; do
    if [ -f "$agent_file" ]; then
        agent_name=$(basename "$agent_file")
        rm -f "$agent_file"
        echo -e "${GREEN}✓ Removed ${agent_name}${NC}"
    fi
done

echo ""
echo -e "${GREEN}AI Proposal Team has been uninstalled.${NC}"
echo ""
echo "Note: Python dependencies were not removed."
echo "To remove them manually:"
echo "  pip uninstall reportlab"
echo ""

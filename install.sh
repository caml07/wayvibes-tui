#!/usr/bin/env bash
set -e

echo "Installing wayvibes-tui..."
echo ""

if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is required but not found."
    exit 1
fi

if ! command -v git &>/dev/null; then
    echo "Error: git is required but not found."
    echo "  Arch/CachyOS: sudo pacman -S git"
    echo "  Ubuntu/Debian: sudo apt install git"
    exit 1
fi

if ! command -v pipx &>/dev/null; then
    echo "Error: pipx is required but not found."
    echo "  Arch/CachyOS: sudo pacman -S python-pipx"
    echo "  Ubuntu/Debian: sudo apt install pipx"
    echo ""
    echo "After installing pipx, you may need to restart your terminal or run:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    exit 1
fi

if ! command -v wayvibes &>/dev/null; then
    echo "Warning: wayvibes is not installed or not in PATH."
    echo "wayvibes-tui requires wayvibes to function."
    echo ""
    echo "Install wayvibes first:"
    echo "  https://github.com/sahaj-b/wayvibes"
    echo ""
    read -r -p "Continue anyway? [y/N] " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
    echo ""
fi

TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

git clone https://github.com/caml07/wayvibes-tui "$TMP_DIR/wayvibes-tui"
cd "$TMP_DIR/wayvibes-tui"

if pipx list | grep -q wayvibes-tui; then
    echo "wayvibes-tui is already installed, upgrading..."
    pipx upgrade wayvibes-tui
else
    pipx install .
fi

echo ""
echo "Done! Run with: wayvibes-tui"
echo ""
echo "If the command is not found, add this to your shell config:"
echo "  Fish:     fish_add_path ~/.local/bin"
echo "  Bash/Zsh: export PATH=\"\$HOME/.local/bin:\$PATH\""
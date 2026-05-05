#!/usr/bin/env bash
set -e

echo "Installing wayvibes-tui..."

if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is required"
    exit 1
fi

if ! command -v pip &>/dev/null; then
    echo "Error: pip is required. Install it with your package manager:"
    echo "  Arch/CachyOS: sudo pacman -S python-pip"
    echo "  Ubuntu/Debian: sudo apt install python3-pip"
    exit 1
fi

if ! command -v wayvibes &>/dev/null; then
    echo "Warning: wayvibes not found in PATH"
    echo "Install it first: https://github.com/sahaj-b/wayvibes"
    echo ""
fi

git clone https://github.com/caml07/wayvibes-tui
cd wayvibes-tui
pip install --user --break-system-packages .

echo ""
echo "Done! Run with: wayvibes-tui"
echo ""
echo "If the command is not found, add this to your shell config:"
echo "  Fish:    fish_add_path ~/.local/bin"
echo "  Bash/Zsh: export PATH=\"\$HOME/.local/bin:\$PATH\""
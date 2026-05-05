#!/usr/bin/env bash
set -e

echo "Installing wayvibes-tui..."

if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is required"
    exit 1
fi

if ! command -v pipx &>/dev/null; then
    echo "Error: pipx is required. Install it with your package manager:"
    echo "  Arch/CachyOS: sudo pacman -S python-pipx"
    echo "  Ubuntu/Debian: sudo apt install pipx"
    exit 1
fi

if ! command -v wayvibes &>/dev/null; then
    echo "Warning: wayvibes not found in PATH"
    echo "Install it first: https://github.com/sahaj-b/wayvibes"
    echo ""
fi

git clone https://github.com/caml07/wayvibes-tui
cd wayvibes-tui
pipx install .

echo ""
echo "Done! Run with: wayvibes-tui"
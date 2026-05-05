#!/usr/bin/env bash
set -e

echo "Installing wayvibes-tui..."

if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is required"
    exit 1
fi

if ! command -v pip &>/dev/null; then
    echo "Error: pip is required"
    exit 1
fi

if ! command -v wayvibes &>/dev/null; then
    echo "Warning: wayvibes not found in PATH"
    echo "Install it first: https://github.com/sahaj-b/wayvibes"
    echo ""
fi

git clone https://github.com/caml07/wayvibes-tui
cd wayvibes-tui
pip install --user .

echo ""
echo "Done! Run with: wayvibes-tui"
echo ""
echo "If the command is not found, add this to your shell config:"
echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
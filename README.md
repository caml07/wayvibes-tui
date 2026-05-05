# wayvibes-tui

A terminal user interface for [wayvibes](https://github.com/sahaj-b/wayvibes) — browse soundpacks, control volume, and manage devices without touching the command line.

![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Requirements

- [wayvibes](https://github.com/sahaj-b/wayvibes) installed and working
- Python 3.11+

---

## Installation

### One liner

```sh
curl -fsSL https://raw.githubusercontent.com/caml07/wayvibes-tui/main/install.sh | bash
```

### Manual

Make sure [wayvibes](https://github.com/sahaj-b/wayvibes) and [pipx](https://pipx.pypa.io) are installed first.

```sh
git clone https://github.com/caml07/wayvibes-tui.git
cd wayvibes-tui
pipx install .
```

If `wayvibes-tui` is not found after installing, add `~/.local/bin` to your PATH:

```sh
# Bash/Zsh
export PATH="$HOME/.local/bin:$PATH"

# Fish
fish_add_path ~/.local/bin
```

---

## Soundpacks

wayvibes-tui expects your soundpacks to be located at:

```
~/wayvibes/soundpacks/
```

Each soundpack should be its own subdirectory inside that folder. If you want to use a different path, edit the config file after the first run:

```
~/.config/wayvibes-tui/config.json
```

---

## Keybindings

| Key | Action |
|-----|--------|
| `s` | Start / Stop wayvibes |
| `]` | Volume up |
| `[` | Volume down |
| `d` | Open device selector |
| `t` | Change theme |
| `q` | Quit |

---

## Configuration

On first launch, a config file is created automatically at `~/.config/wayvibes-tui/config.json`:

```json
{
  "general": {
    "soundpacks_dir": "/home/youruser/wayvibes/soundpacks"
  },
  "wayvibes": {
    "volume": 1.0,
    "input_device": "",
    "output_device": ""
  }
}
```

You can edit this file manually at any time. Changes take effect on the next launch.

---

## Themes

wayvibes-tui comes with the following built-in themes:

- `default` — follows your terminal colors
- `gruvbox`
- `nord`
- `tokyo-night`
- `textual-dark`
- `catppuccin`

The selected theme is saved automatically to `~/.config/wayvibes-tui/config.json`.

---

## Notes

- wayvibes keeps running in the background after you close the TUI. To stop it manually: `pkill wayvibes`
- The TUI reads the current running state on startup, so it will correctly reflect if wayvibes is already active.

---

## Acknowledgements

This project would not exist without [wayvibes](https://github.com/sahaj-b/wayvibes) by [@sahaj-b](https://github.com/sahaj-b) — a clean, minimal mechanical keyboard sound simulator built for Wayland. Go give it a star.

---

## License

MIT
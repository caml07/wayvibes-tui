import subprocess
import os
import signal
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, ListView, ListItem
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from config import load_config, save_config


PID_FILE = Path("/tmp/wayvibes-tui.pid")


def get_output_devices() -> list[str]:
    try:
        result = subprocess.run(
            ["pactl", "list", "sinks", "short"],
            capture_output=True,
            text=True
        )
        devices = []
        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                devices.append(parts[1])
        return devices
    except Exception:
        return []


def is_wayvibes_running() -> bool:
    if not PID_FILE.exists():
        return False
    try:
        pid = int(PID_FILE.read_text().strip())
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, ValueError):
        PID_FILE.unlink(missing_ok=True)
        return False


class DeviceScreen(ModalScreen):

    BINDINGS = [("escape", "dismiss", "Close")]

    def __init__(self, input_devices: list[str], output_devices: list[str], current_input: str, current_output: str):
        super().__init__()
        self.input_devices = input_devices
        self.output_devices = output_devices
        self.current_input = current_input
        self.current_output = current_output
        self.selecting = "input"

    def compose(self) -> ComposeResult:
        with Vertical(id="device-modal"):
            yield Label("── Input Device (keyboard) ──", id="input-title")
            yield ListView(
                ListItem(Label("default"), name=""),
                *[ListItem(Label(d), name=d) for d in self.input_devices],
                id="input-list"
            )
            yield Label("── Output Device (audio) ──", id="output-title")
            yield ListView(
                ListItem(Label("default"), name=""),
                *[ListItem(Label(d), name=d) for d in self.output_devices],
                id="output-list"
            )
            yield Label("ESC to close", id="modal-hint")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        list_id = event.list_view.id
        if list_id == "input-list":
            self.dismiss(("input", event.item.name))
        elif list_id == "output-list":
            self.dismiss(("output", event.item.name))


class WayvibesTUI(App):

    TITLE = "wayvibes-tui"
    SUB_TITLE = "soundpack manager"
    ENABLE_COMMAND_PALETTE = False

    BINDINGS = [
        ("q", "quit", "Exit"),
        ("s", "toggle_wayvibes", "Start/Stop"),
        ("]", "volume_up", "Vol +"),
        ("[", "volume_down", "Vol -"),
        ("d", "change_device", "Devices"),
    ]

    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.soundpacks_dir = Path(self.config["general"]["soundpacks_dir"])
        self.volume = self.config["wayvibes"]["volume"]
        self.input_device = self.config["wayvibes"].get("input_device", "")
        self.output_device = self.config["wayvibes"].get("output_device", "")
        self.active_pack = None

    def get_soundpacks(self) -> list[str]:
        if not self.soundpacks_dir.exists():
            return []
        return [d.name for d in self.soundpacks_dir.iterdir() if d.is_dir()]

    def get_input_devices(self) -> list[str]:
        devices = []

        by_id = Path("/dev/input/by-id")
        if by_id.exists():
            devices += sorted([
                d.name for d in by_id.iterdir()
                if "kbd" in d.name or "keyboard" in d.name.lower()
            ])

        by_path = Path("/dev/input/by-path")
        if by_path.exists():
            devices += sorted([
                d.name for d in by_path.iterdir()
                if "kbd" in d.name
            ])

        return devices

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("Soundpacks")
                packs = self.get_soundpacks()
                if packs:
                    yield ListView(
                        *[ListItem(Label(p), name=p) for p in packs],
                        id="pack-list"
                    )
                else:
                    yield Label("No soundpacks found")
            with Vertical(id="main-panel"):
                yield Label("None selected", id="active-pack")
                yield Label(f"Volume: {self.volume:.1f}", id="volume-label")
                yield Label(f"Input: {self.input_device or 'default'}", id="input-label")
                yield Label(f"Output: {self.output_device or 'default'}", id="output-label")
                running = is_wayvibes_running()
                status = "Status: running ▶" if running else "Status: stopped ■"
                yield Label(status, id="status-label")
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        self.active_pack = event.item.name
        self.query_one("#active-pack", Label).update(f"Pack: {self.active_pack}")

    def action_volume_up(self) -> None:
        if self.volume < 10.0:
            self.volume = round(self.volume + 0.1, 1)
            self._update_volume()

    def action_volume_down(self) -> None:
        if self.volume > 0.0:
            self.volume = round(self.volume - 0.1, 1)
            self._update_volume()

    def _update_volume(self) -> None:
        self.query_one("#volume-label", Label).update(f"Volume: {self.volume:.1f}")
        self.config["wayvibes"]["volume"] = self.volume
        save_config(self.config)

    def action_toggle_wayvibes(self) -> None:
        if is_wayvibes_running():
            self._stop_wayvibes()
        else:
            self._start_wayvibes()

    def _start_wayvibes(self) -> None:
        if not self.active_pack:
            self.query_one("#status-label", Label).update("Status: select a soundpack first")
            return

        pack_path = self.soundpacks_dir / self.active_pack
        cmd = ["wayvibes", str(pack_path), "-v", str(self.volume)]

        if self.input_device:
            cmd += ["--device-name", self.input_device]

        if self.output_device:
            cmd += ["--sink-name", self.output_device]

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        PID_FILE.write_text(str(process.pid))
        self.query_one("#status-label", Label).update("Status: running ▶")

    def _stop_wayvibes(self, update_ui: bool = True) -> None:
        if PID_FILE.exists():
            try:
                pid = int(PID_FILE.read_text().strip())
                os.kill(pid, signal.SIGTERM)
            except (ProcessLookupError, ValueError):
                pass
            PID_FILE.unlink(missing_ok=True)
        if update_ui:
            self.query_one("#status-label", Label).update("Status: stopped ■")

    def action_change_device(self) -> None:
        input_devices = self.get_input_devices()
        output_devices = get_output_devices()

        def on_dismiss(result: tuple | None) -> None:
            if result is None:
                return
            kind, selected = result
            was_running = is_wayvibes_running()

            if kind == "input":
                self.input_device = selected
                self.config["wayvibes"]["input_device"] = selected
                self.query_one("#input-label", Label).update(f"Input: {selected or 'default'}")
            elif kind == "output":
                self.output_device = selected
                self.config["wayvibes"]["output_device"] = selected
                self.query_one("#output-label", Label).update(f"Output: {selected or 'default'}")

            save_config(self.config)

            if was_running:
                self._stop_wayvibes(update_ui=False)
                self._start_wayvibes()
                self.notify("Device changed — wayvibes restarted")

        self.push_screen(
            DeviceScreen(input_devices, output_devices, self.input_device, self.output_device),
            on_dismiss
        )

    def on_unmount(self) -> None:
        pass


def main():
    app = WayvibesTUI()
    app.run()

if __name__ == "__main__":
    main()
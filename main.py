import subprocess
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, ListView, ListItem
from textual.containers import Horizontal, Vertical
from config import load_config, save_config


class WayvibesTUI(App):

    TITLE = "wayvibes-tui"
    SUB_TITLE = "soundpack manager"

    BINDINGS = [
        ("q", "quit", "Exit"),
        ("s", "toggle_wayvibes", "Start/Stop"),
        ("]", "volume_up", "Vol +"),
        ("[", "volume_down", "Vol -"),
    ]

    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.soundpacks_dir = Path(self.config["general"]["soundpacks_dir"])
        self.volume = self.config["wayvibes"]["volume"]
        self.device = self.config["wayvibes"]["device"]
        self.active_pack = None
        self.process = None

    def get_soundpacks(self) -> list[str]:
        if not self.soundpacks_dir.exists():
            return []
        return [d.name for d in self.soundpacks_dir.iterdir() if d.is_dir()]

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
                    yield Label("No se encontraron soundpacks")
            with Vertical(id="main-panel"):
                yield Label("None Selected", id="active-pack")
                yield Label(f"Volumen: {self.volume:.1f}", id="volume-label")
                yield Label(f"Device: {self.device or 'default'}", id="device-label")
                yield Label("Status: stopped", id="status-label")
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
        self.query_one("#volume-label", Label).update(f"Volumen: {self.volume:.1f}")
        self.config["wayvibes"]["volume"] = self.volume
        save_config(self.config)

    def action_toggle_wayvibes(self) -> None:
        if self.process and self.process.poll() is None:
            self._stop_wayvibes()
        else:
            self._start_wayvibes()

    def _start_wayvibes(self) -> None:
        self.notify(f"active_pack = '{self.active_pack}'")
        if not self.active_pack:
            self.query_one("#status-label", Label).update("Status: select a soundpack first")
            return

        pack_path = self.soundpacks_dir / self.active_pack
        cmd = ["wayvibes", str(pack_path), "-v", str(self.volume)]

        if self.device:
            cmd += ["--device-name", self.device]

        self.process = subprocess.Popen(cmd)
        self.query_one("#status-label", Label).update("Status: running ▶")

    def _stop_wayvibes(self, update_ui: bool = True) -> None:
        if self.process:
            self.process.terminate()
            self.process = None
        if update_ui:
          self.query_one("#status-label", Label).update("Status: stopped ■")

    def on_unmount(self) -> None:
        self._stop_wayvibes(update_ui=False)


if __name__ == "__main__":
    app = WayvibesTUI()
    app.run()
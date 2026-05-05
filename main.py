from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label


class WayvibesTUI(App):

    TITLE = "wayvibes-tui"
    SUB_TITLE = "soundpack manager"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("¡Vamos Cam! La TUI está viva 🎹")
        yield Footer()


if __name__ == "__main__":
    app = WayvibesTUI()
    app.run()
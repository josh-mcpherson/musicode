from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TextArea, Static, Button
from textual.containers import Container
from textual.binding import Binding
from textual import events
import json
import os
import multiprocessing
from music import start_music_engine

class MusicodeApp(App):
    CSS_PATH = "musicode.tcss"

    BINDINGS = [
        Binding("d", "toggle_dark", "Toggle dark mode", show=False),
        Binding("q", "quit", "Quit", show=False),
        Binding("p", "toggle_play_pause", "Play/Pause", show=False),
        Binding("escape", "switch_to_edit_mode", "Edit Mode", show=False),
        Binding(":", "switch_to_command_mode", "Command Mode", show=False),
    ]

    def compose(self) -> ComposeResult:
        with open('/home/josh/Code/Musicode/config.json', 'r') as f:
            config = json.load(f)
        
        self.tempo = config.get('tempo', 120)
        self.instrument = config.get('instrument', 'sine')

        self.command_queue = multiprocessing.Queue()
        self.status_queue = multiprocessing.Queue()
        self.music_process = multiprocessing.Process(
            target=start_music_engine,
            args=('/home/josh/Code/Musicode/config.json', self.command_queue, self.status_queue)
        )
        self.music_process.start()

        yield Header()
        self.footer = Footer()
        yield self.footer
        yield Static("", id="mode_instructions")
        yield Container(
            TextArea(open('/home/josh/Code/Musicode/live.mc').read(), id="live_mc_editor"),
            Container(
                Static(f"Tempo: {self.tempo} BPM", id="tempo_display"),
                Static(f"Instrument: {self.instrument}", id="instrument_display"),
                Static("Playing Line: --", id="current_line_display"),
                Button("Play", id="play_pause_button", variant="success"),
                id="side_panel"
            ),
            id="app_grid"
        )

    def on_mount(self) -> None:
        self.set_interval(0.1, self.update_ui_from_music_engine)
        self._mode_instructions_widget = self.query_one("#mode_instructions", Static)
        self.set_mode("edit")

    def set_mode(self, mode: str) -> None:
        self.mode = mode
        if mode == "edit":
            self.query_one("#live_mc_editor", TextArea).focus()
            self.BINDINGS = [
                Binding("d", "toggle_dark", "Toggle dark mode"),
                Binding("escape", "toggle_mode", "Toggle Mode"),
            ]
            self._mode_instructions_widget.update("Press 'Esc' to toggle Command Mode")
            print(f"Edit Mode BINDINGS: {self.BINDINGS}") # Debugging
        elif mode == "command":
            self.query_one("#live_mc_editor", TextArea).blur()
            self.BINDINGS = [
                Binding("escape", "toggle_mode", "Toggle Mode"),
                Binding("p", "toggle_play_pause", "Play/Pause"),
                Binding("s", "save", "Save"),
                Binding("q", "quit", "Quit"),
            ]
            self._mode_instructions_widget.update("Press 'Esc' to toggle Edit Mode | p: Play/Pause | s: Save | q: Quit")
            print(f"Command Mode BINDINGS: {self.BINDINGS}") # Debugging
        self.title = f"Musicode - {mode.upper()} Mode"

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.action_toggle_mode()
            event.prevent_default = True
        elif event.key == "s" and self.mode == "command":
            self.action_save()
            event.prevent_default = True

    def action_toggle_mode(self) -> None:
        if self.mode == "edit":
            self.set_mode("command")
        else:
            self.set_mode("edit")

    def update_ui_from_music_engine(self) -> None:
        if not self.status_queue.empty():
            status = self.status_queue.get()
            line_index = status.get("line_index")
            if line_index is not None:
                self.query_one("#current_line_display", Static).update(f"Playing Line: {line_index + 1}")

    def action_save(self) -> None:
        print("Action: Save triggered")
        text_area = self.query_one("#live_mc_editor", TextArea)
        content = text_area.text
        print(f"Content to save: \n{content[:100]}...") # Print first 100 chars
        try:
            with open('/home/josh/Code/Musicode/live.mc', 'w') as f:
                f.write(content)
            self._mode_instructions_widget.update("Saved!")
            print("File saved successfully.")
        except Exception as e:
            self._mode_instructions_widget.update(f"Save Error: {e}")
            print(f"Error saving file: {e}")
        self.set_timer(2, lambda: self._mode_instructions_widget.update("Press 'Esc' to toggle Edit Mode | p: Play/Pause | s: Save | q: Quit"))

    def action_toggle_play_pause(self) -> None:
        button = self.query_one("#play_pause_button", Button)
        if button.label == "Play":
            button.label = "Pause"
            button.variant = "warning"
            self.command_queue.put("play")
        else:
            button.label = "Play"
            button.variant = "success"
            self.command_queue.put("pause")

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_quit(self) -> None:
        self.command_queue.put("stop") # Send stop command to music engine
        self.music_process.join(timeout=1) # Wait for music process to terminate
        if self.music_process.is_alive():
            self.music_process.terminate() # Force terminate if it doesn't stop gracefully
        self.exit()

if __name__ == "__main__":
    app = MusicodeApp()
    app.run()

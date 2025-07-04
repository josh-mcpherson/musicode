import pygame
import time
import numpy as np

class Musicode:
    def __init__(self, sample_rate=44100, amplitude=4096):
        pygame.mixer.init(frequency=sample_rate)
        self.sample_rate = sample_rate
        self.amplitude = amplitude
        self.NOTES = {
            "C4": 261.63,
            "D4": 293.66,
            "E4": 329.63,
            "F4": 349.23,
            "G4": 392.00,
            "A4": 440.00,
            "B4": 493.88,
            "C5": 523.25,
        }
        self.c_major_scale = list(self.NOTES.items())

    def get_sine_wave(self, frequency, duration):
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        wave = self.amplitude * np.sin(2 * np.pi * frequency * t)
        return np.ascontiguousarray(np.array([wave, wave]).T.astype(np.int16))

    def play_note(self, frequency, duration):
        sound = pygame.sndarray.make_sound(self.get_sine_wave(frequency, duration))
        sound.play()
        time.sleep(duration)

    def play_note_by_name(self, note_name, duration):
        frequency = self.NOTES.get(note_name)
        if frequency:
            self.play_note(frequency, duration)
        else:
            print(f"Note '{note_name}' not found.")

    def play_scale(self, scale, duration=0.5):
        print("Playing the scale...")
        for note_name, frequency in scale:
            print(f"Playing: {note_name}")
            self.play_note(frequency, duration)
        print("Done.")

    def cli(self):
        print("Welcome to Musicode!")
        print("Commands: play [note] [duration], scale, exit")
        while True:
            command = input("> ")
            parts = command.split()
            if not parts:
                continue

            if parts[0] == "play" and len(parts) == 3:
                note_name = parts[1]
                try:
                    duration = float(parts[2])
                    self.play_note_by_name(note_name, duration)
                except ValueError:
                    print("Invalid duration. Please use a number.")
            elif parts[0] == "scale":
                self.play_scale(self.c_major_scale)
            elif parts[0] == "exit":
                break
            else:
                print("Unknown command.")

if __name__ == "__main__":
    music_engine = Musicode()
    music_engine.cli()
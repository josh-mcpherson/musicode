
import pygame
import time
import numpy as np

class Musicode:
    def __init__(self, sample_rate=44100, amplitude=4096):
        pygame.mixer.init(frequency=sample_rate)
        self.sample_rate = sample_rate
        self.amplitude = amplitude
        self.c_major_scale = [
            ("C4", 261.63),
            ("D4", 293.66),
            ("E4", 329.63),
            ("F4", 349.23),
            ("G4", 392.00),
            ("A4", 440.00),
            ("B4", 493.88),
            ("C5", 523.25),
        ]

    def get_sine_wave(self, frequency, duration):
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        wave = self.amplitude * np.sin(2 * np.pi * frequency * t)
        return np.ascontiguousarray(np.array([wave, wave]).T.astype(np.int16))

    def play_note(self, frequency, duration):
        sound = pygame.sndarray.make_sound(self.get_sine_wave(frequency, duration))
        sound.play()
        time.sleep(duration)

    def play_scale(self, scale, duration=0.5):
        print("Playing the scale...")
        for note_name, frequency in scale:
            print(f"Playing: {note_name}")
            self.play_note(frequency, duration)
        print("Done.")

if __name__ == "__main__":
    music_engine = Musicode()
    music_engine.play_scale(music_engine.c_major_scale)

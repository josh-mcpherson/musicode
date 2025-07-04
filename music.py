import pygame
import time
import numpy as np
from scipy.signal import square, sawtooth

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
        self.c_minor_scale = [
            ("C4", 261.63),
            ("D4", 293.66),
            ("Eb4", 311.13),
            ("F4", 349.23),
            ("G4", 392.00),
            ("Ab4", 415.30),
            ("Bb4", 466.16),
            ("C5", 523.25),
        ]
        self.c_major_blues_scale = [
            ("C4", 261.63),
            ("D#4", 311.13),
            ("F4", 349.23),
            ("F#4", 369.99),
            ("G4", 392.00),
            ("A#4", 466.16),
            ("C5", 523.25),
        ]

    def get_sine_wave(self, frequency, duration):
        num_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, num_samples, False)
        wave = self.amplitude * np.sin(2 * np.pi * frequency * t)

        # Apply a fade-in and fade-out to prevent clicking
        fade_duration = 0.01  # 10ms
        fade_len = int(fade_duration * self.sample_rate)
        
        if num_samples > fade_len * 2:
            fade_in = np.linspace(0, 1, fade_len)
            fade_out = np.linspace(1, 0, fade_len)
            wave[:fade_len] *= fade_in
            wave[-fade_len:] *= fade_out

        return np.ascontiguousarray(np.array([wave, wave]).T.astype(np.int16))

    def get_square_wave(self, frequency, duration):
        num_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, num_samples, False)
        wave = self.amplitude * square(2 * np.pi * frequency * t)

        # Apply a fade-in and fade-out to prevent clicking
        fade_duration = 0.01  # 10ms
        fade_len = int(fade_duration * self.sample_rate)
        
        if num_samples > fade_len * 2:
            fade_in = np.linspace(0, 1, fade_len)
            fade_out = np.linspace(1, 0, fade_len)
            wave[:fade_len] *= fade_in
            wave[-fade_len:] *= fade_out

        return np.ascontiguousarray(np.array([wave, wave]).T.astype(np.int16))

    def get_sawtooth_wave(self, frequency, duration):
        num_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, num_samples, False)
        wave = self.amplitude * sawtooth(2 * np.pi * frequency * t)

        # Apply a fade-in and fade-out to prevent clicking
        fade_duration = 0.01  # 10ms
        fade_len = int(fade_duration * self.sample_rate)
        
        if num_samples > fade_len * 2:
            fade_in = np.linspace(0, 1, fade_len)
            fade_out = np.linspace(1, 0, fade_len)
            wave[:fade_len] *= fade_in
            wave[-fade_len:] *= fade_out

        return np.ascontiguousarray(np.array([wave, wave]).T.astype(np.int16))

    def play_note(self, frequency, duration, instrument="sine"):
        if instrument == "square":
            sound = pygame.sndarray.make_sound(self.get_square_wave(frequency, duration))
        elif instrument == "sawtooth":
            sound = pygame.sndarray.make_sound(self.get_sawtooth_wave(frequency, duration))
        else:
            sound = pygame.sndarray.make_sound(self.get_sine_wave(frequency, duration))
        sound.play()
        time.sleep(duration)

    def play_scale(self, scale, duration=0.5, instrument="sine"):
        for note_name, frequency in scale:
            print(f"Playing: {note_name}")
            self.play_note(frequency, duration, instrument)
        print("Done.")

if __name__ == "__main__":
    music_engine = Musicode()
    print("Playing C Major Scale (Sine Wave)...")
    music_engine.play_scale(music_engine.c_major_scale)
    print("\nPlaying C Minor Scale (Sawtooth Wave)...")
    music_engine.play_scale(music_engine.c_minor_scale, instrument="sawtooth")
    print("\nPlaying C Major Blues Scale (Square Wave)...")
    music_engine.play_scale(music_engine.c_major_blues_scale, instrument="square")
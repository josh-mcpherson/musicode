
import pygame
import time
import numpy as np
from scipy.signal import square, sawtooth
import json

class Musicode:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        self.tempo = config.get('tempo', 120)
        self.file_path = config.get('file', 'live.mc')
        self.beat_duration = 60 / self.tempo
        self.default_instrument = config.get('instrument', 'sine')

        pygame.mixer.init(frequency=44100)
        self.sample_rate = 44100
        self.amplitude = 8192
        self.NOTES = {
            'C3': 130.81, 'C#3': 138.59, 'D3': 146.83, 'D#3': 155.56, 'E3': 164.81, 'F3': 174.61, 'F#3': 185.00, 'G3': 196.00, 'G#3': 207.65, 'A3': 220.00, 'A#3': 233.08, 'B3': 246.94,
            'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13, 'E4': 329.63, 'F4': 349.23, 'F#4': 369.99, 'G4': 392.00, 'G#4': 415.30, 'A4': 440.00, 'A#4': 466.16, 'B4': 493.88,
            'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25, 'E5': 659.25, 'F5': 698.46, 'F#5': 739.99, 'G5': 783.99, 'G#5': 830.61, 'A5': 880.00, 'A#5': 932.33, 'B5': 987.77,
        }

    def _apply_amplitude_envelope(self, wave, duration):
        num_samples = len(wave)
        fade_duration = 0.01  # 10ms
        fade_len = int(fade_duration * self.sample_rate)

        if num_samples > fade_len * 2:
            fade_in = np.linspace(0, 1, fade_len)
            fade_out = np.linspace(1, 0, fade_len)
            wave[:fade_len] *= fade_in
            wave[-fade_len:] *= fade_out
        return wave

    def _generate_sine_wave(self, frequency, duration):
        num_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, num_samples, False)
        return self.amplitude * np.sin(2 * np.pi * frequency * t)

    def _generate_square_wave(self, frequency, duration):
        num_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, num_samples, False)
        return self.amplitude * square(2 * np.pi * frequency * t)

    def _generate_sawtooth_wave(self, frequency, duration):
        num_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, num_samples, False)
        return self.amplitude * sawtooth(2 * np.pi * frequency * t)

    def get_wave(self, frequency, duration, instrument='sine'):
        if instrument == 'square':
            wave = self._generate_square_wave(frequency, duration)
        elif instrument == 'sawtooth':
            wave = self._generate_sawtooth_wave(frequency, duration)
        else:  # Default to sine
            wave = self._generate_sine_wave(frequency, duration)

        wave = self._apply_amplitude_envelope(wave, duration)
        return np.ascontiguousarray(np.array([wave, wave]).T.astype(np.int16))

    def play_note_by_name(self, note_name, duration, instrument='sine'):
        frequency = self.NOTES.get(note_name.upper())
        if frequency:
            sound = pygame.sndarray.make_sound(self.get_wave(frequency, duration, instrument))
            sound.play()
        else:
            print(f"Note '{note_name}' not found.")

    def _load_music_file(self):
        try:
            with open(self.file_path, 'r') as f:
                return f.readlines()
        except FileNotFoundError:
            print(f"Error: '{self.file_path}' not found.")
            return []

    def _parse_note_string(self, note_str):
        parts = note_str.split('*')
        note_name = parts[0]
        duration_multiplier = 1.0
        instrument = self.default_instrument

        if len(parts) > 1:
            try:
                duration_multiplier = float(parts[1])
            except ValueError:
                print(f"Warning: Invalid duration multiplier for {note_str}. Using 1.0.")
        if len(parts) > 2:
            instrument = parts[2]
        return note_name, duration_multiplier, instrument

    def _play_line(self, line):
        start_time = time.time()
        notes_to_play = line.strip().split()
        if not notes_to_play:
            pass  # Allow for empty lines representing rests
        else:
            for note_str in notes_to_play:
                note_name, duration_multiplier, instrument = self._parse_note_string(note_str)
                note_duration = self.beat_duration * duration_multiplier
                print(f"Playing {note_name} with {instrument} for {note_duration:.2f}s")
                self.play_note_by_name(note_name, note_duration, instrument)

        # Wait for the beat to finish
        time_spent = time.time() - start_time
        if time_spent < self.beat_duration:
            time.sleep(self.beat_duration - time_spent)

    def play_live(self):
        print(f"Playing '{self.file_path}' at {self.tempo} BPM. Press Ctrl+C to stop.")
        while True:
            try:
                lines = self._load_music_file()
                if not lines:
                    time.sleep(5) # Wait before retrying if file not found
                    continue
                
                for line in lines:
                    self._play_line(line)

            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(5)

if __name__ == "__main__":
    music_engine = Musicode(config_path='/home/josh/Code/Musicode/config.json')
    music_engine.play_live()

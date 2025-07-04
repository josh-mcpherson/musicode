import pygame
import time

# Initialize the pygame mixer
pygame.mixer.init()

# Define the notes of the C major scale
c_major_scale = [
    ("C4", 261.63),
    ("D4", 293.66),
    ("E4", 329.63),
    ("F4", 349.23),
    ("G4", 392.00),
    ("A4", 440.00),
    ("B4", 493.88),
    ("C5", 523.25),
]

def play_note(frequency, duration):
    """Plays a note with a given frequency and duration."""
    sound = pygame.sndarray.make_sound(get_sine_wave(frequency, duration))
    sound.play()
    time.sleep(duration)

def get_sine_wave(frequency, duration, sample_rate=44100, amplitude=4096):
    """Generates a sine wave for a given frequency and duration."""
    import numpy as np
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return np.ascontiguousarray(np.array([wave, wave]).T.astype(np.int16))

if __name__ == "__main__":
    print("Playing the C major scale...")
    for note_name, frequency in c_major_scale:
        print(f"Playing: {note_name}")
        play_note(frequency, 0.5)
    print("Done.")
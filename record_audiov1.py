import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import keyboard

SAMPLE_RATE = 44100
CHANNELS = 2

audio_chunks = []

def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_chunks.append(indata.copy())

print("Press SPACE to start recording...")
keyboard.wait('space')

print("Recording... Press SPACE again to stop.")

with sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    callback=callback
):
    keyboard.wait('space')

print("Recording stopped. Saving file...")

audio_data = np.concatenate(audio_chunks, axis=0)

# Convert float32 to int16 for WAV
audio_data = (audio_data * 32767).astype(np.int16)

write("recorded_audio.wav", SAMPLE_RATE, audio_data)

print("File saved as 'recorded_audio.wav'")
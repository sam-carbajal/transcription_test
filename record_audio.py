import streamlit as st
from streamlit_mic_recorder import mic_recorder
from scipy.io.wavfile import write
import numpy as np

st.title("Audio Recorder")

audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    key="recorder",
)

if audio:
    st.audio(audio["bytes"])

    audio_data = np.frombuffer(audio["bytes"], dtype=np.int16)

    write(
        "recorded_audio.wav",
        audio["sample_rate"],
        audio_data
    )

    st.success("Audio saved!")
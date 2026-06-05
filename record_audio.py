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

filename = "recorded_audio.wav"

if audio:
    st.audio(audio["bytes"])

    audio_data = np.frombuffer(audio["bytes"], dtype=np.int16)

    write(
        filename,
        audio["sample_rate"],
        audio_data
    )

    with open(filename, "rb") as f: #Öffnet die gespeicherte Datei im Binärmodus, weil Audio keine Textdatei ist, sondern rohe Bytes enthält
        st.download_button(
            label="Download Audio (WAV)",
            data=f,
            file_name=filename,
            mime="audio/wav"
        )
    st.success("Audio saved!")

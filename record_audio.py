import os
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from scipy.io.wavfile import write
import numpy as np

st.title("Audio Recorder")
mic_options = {
    "Mikrofon A: Cherry Hochwertiges Studiomikrofon": "mA",
    "Mikrofon B: Wireless Lavalier Interview Mikrofon": "mB",
    "Mikrofon C: Omnidirektionales Konferenzmikrofon": "mC",
    "Mikrofon D: Handy-Mikrofon": "mD"
}

selected_mic = st.selectbox(
    "Wähle dein Mikrofon",
    list(mic_options.keys())
)

mic_key = mic_options[selected_mic]

st.session_state["microphone_key"] = mic_key

if "last_audio_key" not in st.session_state:
    st.session_state["last_audio_key"] = None

audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    key="recorder",
)

filename = f"recorded_audio_{mic_key}.wav"


if audio:
    if st.session_state["last_audio_key"] != filename:
        # neue Aufnahme erkannt → alte Datei löschen
        if os.path.exists(filename):
            os.remove(filename)

    st.session_state["last_audio_key"] = filename
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


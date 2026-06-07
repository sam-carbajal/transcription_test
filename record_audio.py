import streamlit as st
from streamlit_mic_recorder import mic_recorder
from scipy.io.wavfile import write
import numpy as np

st.title("Audio Recorder")

speaker = {
    "Teilnehmende 1": "s1",
    "Teilnehmende 2": "s2",
    "Teilnehmende 3": "s3",
    "Teilnehmende 4": "s4",
    "Teilnehmende 5": "s5",
    "Teilnehmende 6": "s6",
}

selected_speaker = st.selectbox(
    "Wähle die Teilnehmernummer",
    list(speaker.keys())
)

speaker_key = speaker[selected_speaker]

gender = {
    "Mädchen": "f",
    "Junge": "m",
}

selected_gender = st.selectbox(
    "Wähle das Geschlecht des Kindes",
    list(gender.keys())
)

gender_key = gender[selected_gender]

group = {
    "Gruppe 1: Vorgegebene Sätze": "g1",
    "Gruppe 2: Leicht variierte Sätze": "g2",
    "Gruppe 3: Spontane Sprache": "g3",
}

selected_group = st.selectbox(
    "Wähle die Aufnahme-Gruppe",
    list(group.keys())
)

group_key = group[selected_group]

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

if audio:
    st.audio(audio["bytes"], format="audio/mpeg")
    st.audio(audio["bytes"], format="audio/mp4")
    audio_format = "webm"
    filename = f"{speaker_key}_{gender_key}_{group_key}_{mic_key}.{audio_format}"
    # Python Code entscheidet nicht das Format, der Browser entscheidet
    st.write(filename)
    st.write(audio[format])

    with open(filename, "wb") as f:
        f.write(audio["bytes"])  #with open(filename, "rb") as f: #Öffnet die gespeicherte Datei im Binärmodus, weil Audio keine Textdatei ist, sondern rohe Bytes enthält

    st.download_button(
        label="Download Audio (WAV)",
        data=audio["bytes"],
        file_name=filename.replace(".webm", ".wav"),
        mime="audio/wav"
    )

    st.download_button(
        label="Download Audio (WEBM)",
        data=audio["bytes"],
        file_name=filename),
        mime="audio/webm"
    )
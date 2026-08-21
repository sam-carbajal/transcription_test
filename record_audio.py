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


# format="wav" statt der Vorgabe "webm": der Browser liefert dann unkomprimiertes
# PCM statt eines verlustbehaftet kodierten Streams (Safari: MP4/AAC, Chrome:
# WebM/Opus). Das ist fuer die spaetere Messung entscheidend, denn ein
# verlustbehafteter Codec hat keine Bittiefe, begrenzt die Bandbreite je nach
# Browser unterschiedlich und macht Aufnahmen verschiedener Geraete damit
# unvergleichbar. Siehe AUFNAHMEQUALITAET.md.
audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    format="wav",
    key="recorder",
)

def erkenne_format(daten: bytes) -> tuple[str, str]:
    """Bestimmt Endung und MIME-Typ aus den ersten Bytes der Aufnahme.

    Noetig, weil das Python-Skript das Format nicht bestimmt -- der Browser tut
    es. Eine fest vergebene Endung fuehrt sonst zu Dateien, die anders heissen
    als sie sind: Safari liefert MP4/AAC, Chrome und Firefox liefern WebM/Opus.
    Eine solche Datei laesst sich mit vielen Audiobibliotheken (etwa libsndfile,
    und damit soundfile/librosa) gar nicht oeffnen, weil sie sich nach der
    Endung richten oder am unerwarteten Header scheitern.
    """
    if len(daten) >= 12 and daten[4:8] == b"ftyp":
        return "m4a", "audio/mp4"
    if daten[:4] == bytes([0x1A, 0x45, 0xDF, 0xA3]):  # EBML (WebM/Matroska)
        return "webm", "audio/webm"
    if daten[:4] == b"RIFF" and daten[8:12] == b"WAVE":
        return "wav", "audio/wav"
    if daten[:4] == b"OggS":
        return "ogg", "audio/ogg"
    if daten[:3] == b"ID3" or (len(daten) > 1 and daten[0] == 0xFF and daten[1] & 0xE0 == 0xE0):
        return "mp3", "audio/mpeg"
    return "bin", "application/octet-stream"


if audio:
    endung, mime = erkenne_format(audio["bytes"])
    st.audio(audio["bytes"], format=mime)

    filename = f"{speaker_key}_{gender_key}_{group_key}_{mic_key}.{endung}"

    with open(filename, "wb") as f:
        # Binaermodus, weil Audio rohe Bytes enthaelt und keinen Text.
        f.write(audio["bytes"])

    if endung == "wav":
        st.caption(f"Gespeichert als {filename} — unkomprimiertes PCM, "
                   f"Samplerate {audio.get('sample_rate', 'unbekannt')} Hz.")
    else:
        st.warning(
            f"Der Browser hat **{endung.upper()}** geliefert, nicht WAV. Das ist ein "
            f"verlustbehaftetes Format ohne Bittiefe und mit browserabhaengiger "
            f"Bandbegrenzung. Aufnahmen aus verschiedenen Browsern sind dann nur "
            f"eingeschraenkt vergleichbar — siehe AUFNAHMEQUALITAET.md."
        )

    st.download_button(
        label=f"Download Audio ({endung.upper()})",
        data=audio["bytes"],
        file_name=filename,
        mime=mime,
    )
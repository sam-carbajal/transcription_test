import soundfile as sf

def sample_rate():
    data, samplerate = sf.read('audio.wav')
    return samplerate
def bit_tiefe():
    return 16



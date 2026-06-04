# import whisper
# import time
# import librosa

# import torch

# print(torch.cuda.is_available())
# print(torch.cuda.get_device_name(0))


# model = whisper.load_model("small")

# audio_path = r"C:\Users\saman\Documents\Thilio\Technik\Sprachverarbeitung\Audios\F11_07_05_indian.wav"

# # -----------------------------
# # Measure latency (encoder start)
# # -----------------------------
# start_latency = time.time()

# audio = whisper.load_audio(audio_path)

# audio = whisper.pad_or_trim(audio)
# mel = whisper.log_mel_spectrogram(audio).unsqueeze(0).to(model.device)


# _ = model.encoder(mel)

# end_latency = time.time()
# latency = end_latency - start_latency

# # -----------------------------
# # Measure total transcription time
# # -----------------------------
# start_total = time.time()

# result = model.transcribe(audio_path)

# end_total = time.time()
# total_time = end_total - start_total

# # -----------------------------
# # Real-Time Factor (RTF)
# # -----------------------------
# audio_duration = librosa.get_duration(filename=audio_path)
# rtf = total_time / audio_duration

# # -----------------------------
# # Output
# # -----------------------------
# print("Language:", result["language"])
# print("Text:", result["text"])

# print("\n--- Performance ---")
# print(f"Latency (encoder): {latency:.2f} sec")
# print(f"Total time: {total_time:.2f} sec")
# print(f"Audio duration: {audio_duration:.2f} sec")
# print(f"RTF: {rtf:.2f}")

import whisper
import time

model = whisper.load_model("small")

#model = whisper.load_model("base")

audio_path = r"C:\Users\saman\Documents\Thilio\Technik\Sprachverarbeitung\Audios\F11_07_05_indian.wav"

start_total = time.time()

#result = model.transcribe(audio_path)

audio = whisper.load_audio(audio_path)
audio = whisper.pad_or_trim(audio)

mel = whisper.log_mel_spectrogram(audio).to(model.device)

_, probs = model.detect_language(mel)

print(max(probs, key=probs.get))

result = model.transcribe(audio_path)
end_total = time.time()

total_time = end_total - start_total
print(result["text"])

latency = total_time - start_total
print(latency)


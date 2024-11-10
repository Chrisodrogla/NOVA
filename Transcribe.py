import whisper

# recording_AIxadmupSe4uCY1A.mp3

model = whisper.load_model("base")
result = model.transcribe("SilmShady.mp3", fp16=False)

print(result)
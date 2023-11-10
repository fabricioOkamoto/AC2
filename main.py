import openai
from gtts import gTTS
from vosk import Model, KaldiRecognizer
import os
import pyaudio
from io import BytesIO

openai.api_key = "your_api_key"

def text_to_speech(text):
    tts = gTTS(text=text, lang='pt-br') 
    audio = BytesIO()
    tts.save(audio)
    audio.seek(0)
    return audio

def chat(text):
    reply = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Suponha que você é um instrutor de Python."},
            {"role": "user", "content": text},
        ],
        temperature=0.7,
    )
    return reply['choices'][0]['message']['content']

def speech_to_text():
    model = Model("path_to_your_vosk_model")
    recognizer = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

    print("Fale algo:")
    stream.start_stream()
    try:
        while True:
            data = stream.read(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                return result['text']
    except KeyboardInterrupt:
        pass
    finally:
        print("Parando a gravação...")
        stream.stop_stream()
        stream.close()
        p.terminate()

    return ""

while True:
    user_input = input("Escreva ou fale algo: ")

    if user_input.lower() == 'falar':
        spoken_input = speech_to_text()
        print("Você disse: " + spoken_input)
        response = chat(spoken_input)
        print("Bot: " + response)
        audio_response = text_to_speech(response)
        # Play the audio_response using your preferred method (e.g., a library like pygame or pydub)
        # You need to implement the audio playback part based on your specific requirements.
    else:
        response = chat(user_input)
        print("Bot: " + response)
        audio_response = text_to_speech(response)
        # Play the audio_response using your preferred method (e.g., a library like pygame or pydub)
        # You need to implement the audio playback part based on your specific requirements.

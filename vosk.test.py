from vosk import Model, KaldiRecognizer
import os
import pyaudio
import openai

openai.api_key = "ap"


def chat(texto):
    respostab = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Suponha que você é um instrutor de Python."},
            {"role": "user", "content": texto}],
        temperatura=0.7)
    return resposta['choices'][0]['message']['content']

def ouvir():
    model = Model("caminho_para_modelo_vosk")
    recognizer = KaldiRecognizer(model, 16000)

    play = pyaudio.PyAudio()
    start = play.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    print("fale:")
    start.start_stream()
    try:
        while True:
            data = start.read(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                return result('text')
    except KeyboardInterrupt:
        pass
    finally:
        print("gravação encerrada...")
        stream.stop_stream()
        stream.close()
        play.terminate()
      return ""

while True:
    pergunta = ouvir()
    if pergunta:
        resposta_chatgpt = conversar(pergunta)
        print("Jarvis: " + resposta_chatgpt)

import os
import logging
import whisper

# Carregar modelo Whisper (pode ser "tiny", "base", "small", "medium" ou "large")
model = whisper.load_model("base")

def transcribe_audio(file_path):
    """
    Transcreve um arquivo de áudio usando Whisper.
    :param file_path: Caminho do arquivo de áudio.
    :return: Texto transcrito.
    """
    result = model.transcribe(f"{os.getcwd()}/{file_path}")
    print(result["text"])
    return result["text"]

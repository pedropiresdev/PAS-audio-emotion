import logging

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import uuid
from pathlib import Path
import librosa
import numpy as np
import pickle

import uvicorn
import metrics

from backend.src.transcriptor import transcribe_audio

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()

#! Configuração do CORS para permitir requisições frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "models/svm_emotion.pkl"

# Carregar modelo treinado
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
else:
    raise RuntimeError("Modelo SVM não encontrado. Execute `train_svm.py` primeiro!")


def extract_features(file):
    """
    Extrai características do áudio para análise.
    MFCCs (Mel-Frequency Cepstral Coefficients): Representam o espectro do áudio, úteis para reconhecimento de fala.
    Chroma: Mede a intensidade das notas musicais.
    Mel Spectrogram: Representação do espectrograma de frequência.
    Spectral Contrast: Mede a diferença entre picos e vales no espectro.
    """
    y, sr = librosa.load(file, sr=None)
    mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(y=y, sr=sr).T, axis=0)
    return np.hstack([mfccs, chroma, mel])

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Processa o áudio, realiza transcrição e analisa a emoção detectada.
    """
    try:
        # Salvar arquivo temporário
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Transcrever áudio
        transcription = transcribe_audio(temp_path)

        # Extrair características e prever emoção
        features = extract_features(temp_path)
        emotion_prediction = model.predict([features])[0]
        print(emotion_prediction)

        # Remover arquivo temporário
        os.remove(temp_path)

        return JSONResponse(content={
            "file_name": file.filename,
            "transcription": transcription,
            "predicted_emotion": emotion_prediction
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# Simulação de análise de emoções no áudio
# def analyze_audio(file_path: str):
#     return process_file(file_path)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
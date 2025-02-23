from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import uuid
from pathlib import Path

import uvicorn

from backend.src.transcriptor import process_file

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

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Salvar o arquivo com um nome único
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Simula a análise do áudio/vídeo
        emotion_result = analyze_audio(file_path)

        return JSONResponse(content={"message": "Upload bem-sucedido", "emotion": emotion_result})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# Simulação de análise de emoções no áudio
def analyze_audio(file_path: str):
    return process_file(file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

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

app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Verifica extensão do arquivo
    allowed_extensions = {".mp3", ".wav", ".mp4", ".avi", ".mov"}
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=405, detail="Extensão de arquivo não permitida.")

    # Caminho onde o arquivo será salvo
    file_path = UPLOAD_DIR / file.filename

    # Escreve o arquivo no disco
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {"filename": file.filename, "message": "Upload realizado com sucesso."}

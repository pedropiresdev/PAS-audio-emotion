import os
import whisper
import librosa
import numpy as np
import soundfile as sf
import joblib
from openai import OpenAI

from moviepy import AudioFileClip, VideoFileClip
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# Carregar modelo Whisper para transcrição
model = whisper.load_model("base")
client = OpenAI(api_key="")


def extract_audio(input_file):
    """
    Extrai o áudio de um vídeo se necessário.
    """
    if input_file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        video = VideoFileClip(input_file)
        audio_path = "temp_audio.wav"
        video.audio.write_audiofile(audio_path)
        return audio_path
    return input_file


def transcribe_audio(audio_path):
    """Transcreve o áudio usando Whisper."""
    audio_file = open(f"{os.getcwd()}/{audio_path}", "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1",file=audio_file)
    result = model.transcribe()
    return result['text']


def extract_features(audio_path):
    """Extrai características do áudio para análise de sentimento."""
    y, sr = librosa.load(audio_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    mel = librosa.feature.melspectrogram(y=y, sr=sr)
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

    features = np.hstack([
        np.mean(mfccs, axis=1),
        np.mean(chroma, axis=1),
        np.mean(mel, axis=1),
        np.mean(contrast, axis=1)
    ])
    return features


def train_emotion_classifier():
    """Treina um classificador SVM para emoções (exemplo com dados simulados)."""
    emotions = ['feliz', 'triste', 'raiva', 'surpreso', 'neutro']

    # Simulação de dados de treinamento. Preciso substituir por um dataset real.
    X_train = np.random.rand(100, 40)  # 100 amostras, 40 features cada
    y_train = np.random.choice(emotions, 100)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)

    clf = SVC(kernel='linear', probability=True)
    clf.fit(X_train, y_train)

    joblib.dump((clf, scaler), "emotion_model.pkl")
    print("Modelo de emoções treinado e salvo!")


def predict_emotion(audio_path):
    """Prediz a emoção do áudio com base nas características extraídas."""
    emotions = ['feliz', 'triste', 'raiva', 'surpreso', 'neutro']

    if not os.path.exists("emotion_model.pkl"):
        train_emotion_classifier()

    clf, scaler = joblib.load("emotion_model.pkl")

    features = extract_features(audio_path).reshape(1, -1)
    features = scaler.transform(features)

    prediction = clf.predict(features)[0]
    return prediction


def process_file(file_path):
    """Processa o arquivo para transcrição e análise de sentimentos."""
    audio_path = extract_audio(file_path)
    text = transcribe_audio(audio_path)
    emotion = predict_emotion(audio_path)

    print("Transcrição:", text)
    print("Emoção detectada:", emotion)

    if os.path.exists("temp_audio.wav"):
        os.remove("temp_audio.wav")  # Remove o arquivo temporário

    return text, emotion

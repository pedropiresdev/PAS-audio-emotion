import os
import librosa
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# Lista de emoções esperadas no dataset RAVDESS
EMOTIONS = {
    "01": "neutro",
    "02": "calmo",
    "03": "feliz",
    "04": "triste",
    "05": "raiva",
    "06": "medo",
    "07": "nojo",
    "08": "surpreso"
}

DATASET_PATH = "datasets/RAVDESS"
MODEL_PATH = "models/svm_emotion.pkl"


def extract_features(file_path):
    """
    Extrai características do áudio: MFCCs, Chroma e Mel Spectrogram.
    """
    y, sr = librosa.load(file_path, sr=None)

    mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(y=y, sr=sr).T, axis=0)

    return np.hstack([mfccs, chroma, mel])


def load_data():
    """
    Carrega os áudios do dataset, extrai características e cria rótulos.
    """
    X, y = [], []

    for root, _, files in os.walk(DATASET_PATH):
        for file in files:
            if file.endswith(".wav"):
                emotion_code = file.split("-")[2]
                if emotion_code in EMOTIONS:
                    feature_vector = extract_features(os.path.join(root, file))
                    X.append(feature_vector)
                    y.append(EMOTIONS[emotion_code])

    return np.array(X), np.array(y)


def train_svm():
    """
    Treina um classificador SVM para análise de emoções.
    """
    print("Carregando dataset...")
    X, y = load_data()

    print("Dividindo em treino e teste...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Treinando o modelo SVM...")
    model = make_pipeline(StandardScaler(), SVC(kernel="rbf", probability=True))
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print(f"Modelo treinado com acurácia: {accuracy:.4f}")

    print("Salvando modelo...")
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("Treinamento concluído!")


if __name__ == "__main__":
    train_svm()

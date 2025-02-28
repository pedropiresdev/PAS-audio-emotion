from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np

# Lista de emoções possíveis no modelo
EMOTIONS = ["feliz", "triste", "raiva", "medo", "neutro", "surpreso", "nojo"]

def evaluate_model(y_true, y_pred):
    """
    Avalia a precisão do modelo de análise de emoções.
    :param y_true: Lista de emoções reais (labels corretos).
    :param y_pred: Lista de emoções previstas pelo modelo.
    :return: Dicionário com métricas de acurácia.
    """
    accuracy = accuracy_score(y_true, y_pred)
    report = classification_report(y_true, y_pred, target_names=EMOTIONS, output_dict=True)
    conf_matrix = confusion_matrix(y_true, y_pred)

    return {
        "accuracy": round(accuracy, 4),
        "classification_report": report,
        "confusion_matrix": conf_matrix.tolist()
    }

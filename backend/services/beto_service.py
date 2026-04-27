import re
import torch
import numpy as np
from transformers import BertTokenizerFast, BertForSequenceClassification
from pathlib import Path

# ── Ruta al modelo (relativa al archivo actual) ──────────────────────────────
MODEL_DIR = Path(__file__).parent.parent / "beto_fakenews_model"
MAX_LEN   = 512 

# ── Carga única al iniciar el proceso (no en cada request) ───────────────────

_tokenizer = None
_model = None
_load_error = None
try:
    print(f"[BETO] Cargando modelo desde {MODEL_DIR}...")
    _tokenizer = BertTokenizerFast.from_pretrained(str(MODEL_DIR))
    _model     = BertForSequenceClassification.from_pretrained(str(MODEL_DIR))
    _model.eval()
    print("[BETO] Modelo listo.")
except Exception as e:
    _load_error = str(e)
    print(f"[BETO] ERROR al cargar el modelo: {_load_error}")

# ── Helpers ───────────────────────────────────────────────────────────────────
def _limpiar(texto: str) -> str:
    texto = re.sub(r"http\S+", "", texto)
    texto = re.sub(r"<.*?>", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return " ".join(texto.split()[:380]).strip()

def _shap_flags(texto: str, probs: list[float]) -> list[dict]:
    """
    SHAP real requiere la librería 'shap' y puede ralentizar bastante la API.
    Un texto de ~100 palabras en BERT CPU puede tardar 30 segundos a varios minutos por request
    Por ahora implementé de forma sencilla unaheurística basada en palabras clave de alto impacto.

    Reemplazable con shap.Explainer en el futuro.

    Estas palabras clave y sus puntajes de impacto son ejemplos que se utilizaron en el entrenamiento
    del modelo BETO para detectar noticias falsas. En un modelo real, estos puntajes se derivarían de 
    los valores SHAP calculados.
    """
    KEYWORDS = {
        "urgente": 0.9, "exclusivo": 0.85, "ocultan": 0.8,
        "descubren": 0.75, "comparte": 0.7, "antes de que lo borren": 0.95,
        "fuentes anónimas": 0.7, "confirmó": 0.5, "científicos": 0.4,
    }
    palabras = texto.lower()
    flags = []
    for palabra, impacto in KEYWORDS.items():
        if palabra in palabras:
            flags.append({"word": palabra, "impact_score": round(impacto * probs[0], 3)})
    return sorted(flags, key=lambda x: x["impact_score"], reverse=True)[:5]


# ── Función principal (mismo contrato que el mock) ────────────────────────────
def analyze_style(text: str) -> dict:
    if _load_error is not None or _tokenizer is None or _model is None:
        return {
            "engine": "BETO NLP (ERROR)",
            "error": f"No se pudo cargar el modelo BETO: {_load_error if _load_error else 'Desconocido'}",
            "fake_probability_score": None,
            "shap_flags": [],
        }
    try:
        texto_limpio = _limpiar(text)
        enc = _tokenizer(
            texto_limpio,
            max_length=MAX_LEN,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        with torch.no_grad():
            logits = _model(**enc).logits
        probs = torch.softmax(logits, dim=1).squeeze().tolist()
        fake_score = round(probs[0] * 100, 2)
        return {
            "engine": "BETO NLP CUSTOM",
            "fake_probability_score": fake_score,
            "shap_flags": _shap_flags(texto_limpio, probs),
        }
    except Exception as e:
        return {
            "engine": "BETO NLP (ERROR)",
            "error": f"Error al analizar el texto: {str(e)}",
            "fake_probability_score": None,
            "shap_flags": [],
        }
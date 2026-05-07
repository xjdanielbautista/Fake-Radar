"""
fake_radar_service.py
=====================
Servicio de análisis de noticias usando el modelo fake_radar_v5.
Reemplaza a beto_service.py (ver ese archivo para el historial anterior).

Cambios respecto a BETO:
  - Modelo: RoBERTa (fine-tuned) en vez de BERT
  - Tokenizer: AutoTokenizer en vez de BertTokenizerFast
  - MAX_LEN: 256 (igual que en entrenamiento)
  - Bug fix: fake_score ahora usa probs[1] (clase Fake) en vez de probs[0] (clase Real)
  - Se añade campo 'verdict' con umbral claro
  - Misma interfaz pública: analyze_style(text) → dict
"""

import re
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

# Ruta al modelo v5 (relativa a este archivo)
# Estructura esperada: backend/fake_radar_v5/config.json, model.safetensors, etc.
MODEL_DIR = Path(__file__).parent.parent / "fake_radar_v5"
MAX_LEN   = 256   # Debe coincidir con MAX_LENGTH usado en entrenamiento

# Umbrales de decisión para el veredicto
THRESHOLD_FAKE = 0.65   # >= 65% → Falso
THRESHOLD_REAL = 0.40   # <= 40% → Verdadero
                        #  Entre 40% y 65% → Dudoso

# =============================================================================
# CARGA DEL MODELO (única vez al iniciar el proceso)
# =============================================================================

_tokenizer  = None
_model      = None
_load_error = None
_device     = "cuda" if torch.cuda.is_available() else "cpu"

try:
    print(f"[FakeRadar V5] Cargando modelo desde {MODEL_DIR}...")
    print(f"[FakeRadar V5] Dispositivo: {_device.upper()}")

    _tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR))
    _model     = AutoModelForSequenceClassification.from_pretrained(str(MODEL_DIR))
    _model.to(_device)
    _model.eval()

    print("[FakeRadar V5] ✓ Modelo listo.")
except Exception as e:
    _load_error = str(e)
    print(f"[FakeRadar V5] ✗ ERROR al cargar el modelo: {_load_error}")


# =============================================================================
# HELPERS PRIVADOS
# =============================================================================

def _limpiar(texto: str) -> str:
    """Limpia URLs, HTML y espacios extra del texto."""
    texto = re.sub(r"http\S+", "", texto)
    texto = re.sub(r"<.*?>", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def _get_verdict(fake_score: float) -> str:
    """
    Convierte el puntaje numérico en un veredicto legible.
    fake_score está en escala 0-100.
    """
    if fake_score >= THRESHOLD_FAKE * 100:
        return "Falso"
    elif fake_score <= THRESHOLD_REAL * 100:
        return "Verdadero"
    else:
        return "Dudoso"


def _get_linguistic_flags(texto: str, fake_score: float) -> list[dict]:
    """
    Heurística de palabras clave de alto impacto en noticias falsas.
    Devuelve las 5 palabras más sospechosas encontradas en el texto.

    Nota: Reemplazable con SHAP real en el futuro (requiere pip install shap,
    pero añade ~30s por request en CPU — no recomendado en producción aún).
    """
    KEYWORDS = {
        "urgente":                0.90,
        "exclusivo":              0.85,
        "ocultan":                0.80,
        "antes de que lo borren": 0.95,
        "fuentes anónimas":       0.70,
        "descubren":              0.75,
        "comparte":               0.70,
        "confirmó":               0.50,
        "científicos":            0.40,
        "alerta":                 0.65,
        "censurado":              0.88,
        "prohibido":              0.72,
        "te ocultan":             0.92,
        "la verdad sobre":        0.80,
        "médicos no quieren":     0.95,
    }

    texto_lower = texto.lower()
    flags = []

    for keyword, base_impact in KEYWORDS.items():
        if keyword in texto_lower:
            # El impacto real se pondera por el score de falsedad del modelo
            impact = round(base_impact * (fake_score / 100), 3)
            flags.append({"word": keyword, "impact_score": impact})

    return sorted(flags, key=lambda x: x["impact_score"], reverse=True)[:5]


# =============================================================================
# FUNCIÓN PÚBLICA (misma interfaz que beto_service.py)
# =============================================================================

def analyze_style(text: str) -> dict:
    """
    Analiza un texto y retorna el puntaje de falsedad + flags lingüísticos.

    Retorna:
        dict con campos:
          - engine: nombre del motor
          - fake_probability_score: float 0-100 (100 = muy probablemente falso)
          - verdict: "Falso" | "Dudoso" | "Verdadero"
          - shap_flags: lista de palabras clave sospechosas encontradas
          - error: string (solo si falló)
    """
    if _load_error is not None or _tokenizer is None or _model is None:
        return {
            "engine":                 "FakeRadar V5 (ERROR)",
            "error":                  f"Modelo no disponible: {_load_error or 'Desconocido'}",
            "fake_probability_score": None,
            "verdict":                "No disponible",
            "shap_flags":             [],
        }

    try:
        texto_limpio = _limpiar(text)

        # Tokenización (igual que en entrenamiento)
        enc = _tokenizer(
            texto_limpio,
            max_length=MAX_LEN,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )

        # Mover inputs al mismo dispositivo que el modelo
        enc = {k: v.to(_device) for k, v in enc.items()}

        with torch.no_grad():
            logits = _model(**enc).logits

        probs = torch.softmax(logits, dim=1).squeeze().tolist()

        # IMPORTANTE: label 0 = Real, label 1 = Fake (según entrenamiento)
        # probs[0] = probabilidad de ser REAL
        # probs[1] = probabilidad de ser FALSA  ← este es el score correcto
        fake_score = round(probs[1] * 100, 2)
        verdict    = _get_verdict(fake_score)

        return {
            "engine":                 "FakeRadar V5 (RoBERTa)",
            "fake_probability_score": fake_score,
            "verdict":                verdict,
            "shap_flags":             _get_linguistic_flags(texto_limpio, fake_score),
        }

    except Exception as e:
        return {
            "engine":                 "FakeRadar V5 (ERROR)",
            "error":                  f"Error al analizar: {str(e)}",
            "fake_probability_score": None,
            "verdict":                "No disponible",
            "shap_flags":             [],
        }

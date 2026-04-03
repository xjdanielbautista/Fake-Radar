def analyze_style(text: str) -> dict:
    """
    Simulador del modelo BETO NLP. 
    Se reemplazará con el modelo real cuando esté disponible.
    """
    return {
        "engine": "BETO NLP (Mock Preparado)",
        "fake_probability_score": 85.5,
        "shap_flags": [
            {"word": "urgente", "impact_score": 0.9},
            {"word": "ocultan", "impact_score": 0.8},
            {"word": "inconclusos", "impact_score": 0.6}
        ]
    }
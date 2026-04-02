# uvicorn main:app --reload, that's the command to run this backend server in development mode. It will auto-reload on code changes.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

# Importacion de modelos y servicio de AI
from models import AnalyzeRequest, AnalyzeResponse
from services.ai_service import generate_response

# Se crea la instancia de FastAPI
app = FastAPI(
    title="Fake Radar API",
    description="API para detección de desinformación. Motor Stateless.",
    version="1.1.0"
)

# Configuración de CORS: Esto es vital para que el Frontend (React) 
# y la extension de Chrome puedan hablar con este backend sin que el navegador los bloquee.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de prueba para verificar que el backend está funcionando correctamente. Devuelve un mensaje simple en formato JSON.
@app.get("/")
async def root():
    return {"message": "El backend de Fake Radar esta en linea."}

# EL ENDPOINT PRINCIPAL: /analyze
@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_news(request: AnalyzeRequest):

    # Se arman las instrucciones (Prompt) obligando a Gemini a respetar la estructura de Pydantic
    prompt = f"""
    Eres un experto en detección de desinformación. Analiza la siguiente noticia y devuelve un JSON estricto.
    Noticia: {request.text}
    
    El JSON DEBE tener exactamente esta estructura y usar estas llaves:
    {{
      "status": "success",
      "global_assessment": "Dudoso",
      "analysis": {{
        "style_analysis": {{
          "engine": "BETO NLP",
          "fake_probability_score": 50.0,
          "shap_flags": [
            {{"word": "ejemplo", "impact_score": 0.5}}
          ]
        }},
        "fact_check_analysis": {{
          "engine": "Gemini API + Web Search",
          "verdict": "Requiere verificación",
          "reasoning": "Escribe aquí tu razonamiento analizando los hechos de la noticia.",
          "references": [
            {{"title": "Fuente de ejemplo", "url": "https://ejemplo.com", "domain": "ejemplo.com"}}
          ]
        }}
      }}
    }}
    """
    
    # Se ejecuta el servicio de IA con el prompt construido. Se espera un texto que sea un JSON, pero si algo falla, se devuelve un diccionario de error.
    raw_response = generate_response(prompt)
    
    # Se maneja el caso de error en la generación de la respuesta. Si el servicio de IA falla, se devuelve un JSON con un mensaje de error en el campo "reasoning" del análisis de hechos.
    if isinstance(raw_response, dict) and "error" in raw_response:
        return {
            "status": "error",
            "global_assessment": "Error en el servidor de IA",
            "analysis": {
                "style_analysis": {"engine": "BETO NLP", "fake_probability_score": 0.0, "shap_flags": []},
                "fact_check_analysis": {"engine": "Gemini API", "verdict": "Error", "reasoning": raw_response["error"], "references": []}
            }
        }

    # Se intenta parsear la respuesta cruda de texto a un diccionario. Si el formato no es correcto, se devuelve un JSON con un mensaje de error en el campo "reasoning" del análisis de hechos.
    try:
        parsed_data = json.loads(raw_response)
        return parsed_data
    except json.JSONDecodeError:
        return {
            "status": "error",
            "global_assessment": "Error de formato",
            "analysis": {
                "style_analysis": {"engine": "BETO NLP", "fake_probability_score": 0.0, "shap_flags": []},
                "fact_check_analysis": {"engine": "Gemini API", "verdict": "Error", "reasoning": "La IA no devolvió un JSON válido.", "references": []}
            }
        }
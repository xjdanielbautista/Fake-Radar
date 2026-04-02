# uvicorn main:app --reload, that's the command to run this backend server in development mode. It will auto-reload on code changes.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

# Importacion de modelos y servicio de AI
from models import AnalyzeRequest, AnalyzeResponse
from services.ai_service import generate_response
from services.beto_service import analyze_style

# Se crea la instancia de FastAPI
app = FastAPI(
    title="Fake Radar API",
    description="API para detección de desinformación. Motor Stateless.",
    version="1.2.0"
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

    # Se ejecuta el análisis de estilo con BETO (mock por ahora)
    beto_data = analyze_style(request.text)
    
    # Se construye el prompt para gemini, incluyendo el texto de la noticia y las instrucciones claras para el JSON valido
    prompt = f"""
    Eres un experto en detección de desinformación. Analiza la siguiente noticia y devuelve un JSON estricto.
    Noticia: {request.text}
    
    El JSON DEBE tener exactamente esta estructura y usar estas llaves:
    {{
      "global_assessment": "Dudoso",
      "fact_check_analysis": {{
        "engine": "Gemini API + Web Search",
        "verdict": "Requiere verificación",
        "reasoning": "Escribe aquí tu razonamiento analizando los hechos.",
        "references": [
          {{"title": "Fuente", "url": "https://ejemplo.com", "domain": "ejemplo.com"}}
        ]
      }}
    }}
    """
    
    # Se llama a la funcion que se comunica con gemini API
    raw_response = generate_response(prompt)
    
    # Validacion y manejo de errores para asegurar que el backend siempre devuelve un JSON con la estructura correcta, incluso si Gemini falla o devuelve algo inesperado.
    if isinstance(raw_response, dict) and "error" in raw_response:
        gemini_data = {
            "global_assessment": "Error en el servidor de IA",
            "fact_check_analysis": {
                "engine": "Gemini API", "verdict": "Error", "reasoning": raw_response["error"], "references": []
            }
        }
    else:
        try:
            gemini_data = json.loads(raw_response)
        except json.JSONDecodeError:
            gemini_data = {
                "global_assessment": "Error de formato",
                "fact_check_analysis": {
                    "engine": "Gemini API", "verdict": "Error", "reasoning": "La IA no devolvió un JSON válido.", "references": []
                }
            }

    # Fusion de los resultados de BETO y gemini en una respuesta final.
    final_response = {
        "status": "success",
        "global_assessment": gemini_data.get("global_assessment", "Desconocido"),
        "analysis": {
            "style_analysis": beto_data,
            "fact_check_analysis": gemini_data.get("fact_check_analysis", {})
        }
    }
    
    return final_response
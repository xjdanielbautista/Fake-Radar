# uvicorn main:app --reload, that's the command to run this backend server in development mode. It will auto-reload on code changes.

import logging
import os
from datetime import datetime
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
import json

# Importacion de modelos y servicio de AI
from models import AnalyzeRequest, AnalyzeResponse
from services.ai_service import generate_response
from services.beto_service import analyze_style

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Se crea la instancia de FastAPI
app = FastAPI(
    title="Fake Radar API",
    description="API para detección de desinformación. Motor Stateless.",
    version="1.2.1"
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

    # Se ejecuta el análisis de estilo con BETO
    beto_data = analyze_style(request.text)
    
    # Se construye el prompt para gemini, incluyendo el texto de la noticia y las instrucciones claras para el JSON valido
    prompt = f"""
        Eres un experto en detección de desinformación y fact-checking periodístico.

        Analiza la siguiente noticia y responde ÚNICAMENTE con un objeto JSON válido, sin texto adicional, sin bloques de código markdown.

        NOTICIA:
        {request.text}

        INSTRUCCIONES:
        - global_assessment debe ser exactamente uno de: "Verdadero", "Dudoso", "Falso"
        - verdict debe ser exactamente uno de: "Verificado", "Falso", "Engañoso", "Requiere verificación", "No verificable"
        - reasoning debe explicar: qué afirmaciones concretas hace la noticia, qué evidencia existe a favor o en contra, y por qué se asignó ese veredicto
        - references debe incluir fuentes reales y relevantes que respalden el análisis (mínimo 1, máximo 5)
        - Si no encuentras fuentes confiables, usa una lista vacía en references

        ESTRUCTURA JSON REQUERIDA:
        {{
        "global_assessment": "<valor>",
        "fact_check_analysis": {{
            "engine": "Gemini API",
            "verdict": "<valor>",
            "reasoning": "<análisis detallado>",
            "references": [
            {{"title": "<título de la fuente>", "url": "<url>", "domain": "<dominio>"}}
            ]
        }}
        }}
        """
    
    # Se llama a la funcion que se comunica con gemini API
    raw_response = generate_response(prompt)
    
    # Validacion y manejo de errores para asegurar que el backend siempre devuelve un JSON con la estructura correcta, incluso si Gemini falla o devuelve algo inesperado.
    if isinstance(raw_response, dict):
        if "error" in raw_response:
            gemini_data = {
                "global_assessment": "Error en el servidor de IA",
                "fact_check_analysis": {
                    "engine": "Gemini API", "verdict": "Error", "reasoning": raw_response["error"], "references": []
                }
            }
        else:
            # generate_response returned a dict directly — use it as-is
            gemini_data = raw_response
    elif isinstance(raw_response, str):
        try:
            gemini_data = json.loads(raw_response)
        except json.JSONDecodeError:
            gemini_data = {
                "global_assessment": "Error de formato",
                "fact_check_analysis": {
                    "engine": "Gemini API", "verdict": "Error", "reasoning": "La IA no devolvió un JSON válido.", "references": []
                }
            }
    else:
        # None or unexpected type
        gemini_data = {
            "global_assessment": "Error en el servidor de IA",
            "fact_check_analysis": {
                "engine": "Gemini API", "verdict": "Error", "reasoning": f"Tipo de respuesta inesperado: {type(raw_response)}", "references": []
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

# Health check endpoint para monitoreo y logs de acceso.
@app.get("/gemini-status")
async def gemini_status(request: Request, response: Response):
    """Gemini API endpoint for monitoring."""

    timestamp = datetime.now().strftime("%H:%M:%S")
    client_ip = request.client.host

    api_key = os.getenv("GEMINI_API_KEY")
    gemini_status = "Up" if api_key else "Down"
    
    logger.info(f"[{timestamp}] | IP: {client_ip} | Gemini: {gemini_status} | Status: {'OK' if api_key else 'Error'}")
    
    if not api_key:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "Error", "message": "GEMINI_API_KEY is not set. Gemini API is down."}
    
    return {"status": "OK", "message": "API is operational"}
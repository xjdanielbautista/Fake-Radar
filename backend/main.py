# uvicorn main:app --reload, that's the command to run this backend server in development mode. It will auto-reload on code changes.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import AnalyzeRequest, AnalyzeResponse

# Se crea la instancia de FastAPI
app = FastAPI(
    title="Fake Radar API",
    description="API para detección de desinformación. Motor Stateless.",
    version="1.0.0"
)

# Configuración de CORS: Esto es vital para que el Frontend (React) 
# y la extension de Chrome puedan hablar con este backend sin que el navegador los bloquee.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Por ahora aceptamos peticiones de cualquier lado
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de prueba
@app.get("/")
async def root():
    return {"message": "El backend de Fake Radar esta en linea."}

# EL ENDPOINT PRINCIPAL: Aquí es donde pega el Frontend
@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_news(request: AnalyzeRequest):
    # Aqui se programara la logica para ejecutar a BETO y la llamada a Gemini. 
    # Por ahora, solo devolvemos un JSON de prueba (Mock) para que el Frontend 
    # y la Extensión puedan avanzar con el diseño.
    
    # JSON de prueba (Mock) para que el Frontend y la Extensión puedan avanzar con el diseño
    mock_response = {
        "status": "success",
        "global_assessment": "Falso",
        "analysis": {
            "style_analysis": {
                "engine": "BETO NLP",
                "fake_probability_score": 92.5,
                "shap_flags": [
                    {"word": "¡ESCÁNDALO!", "impact_score": 0.45},
                    {"word": "secreto", "impact_score": 0.15},
                    {"word": "fraude", "impact_score": 0.25},
                    {"word": "¡Difunde", "impact_score": 0.35}
                ]
            },
            "fact_check_analysis": {
                "engine": "Gemini API + Web Search",
                "verdict": "Desinformación",
                "reasoning": "No existe ningún documento oficial ni reporte periodístico verificado sobre un fraude admitido por el INE en Baja California. Las fuentes oficiales confirman la normalidad del proceso electoral.",
                "references": [
                    {
                        "title": "Verificado MX: Falso que el INE admitiera fraude en BC",
                        "url": "https://verificado.com.mx/falso-fraude-ine-bc",
                        "domain": "verificado.com.mx"
                    },
                    {
                        "title": "INE Baja California: Comunicado Oficial",
                        "url": "https://ine.mx/baja-california/comunicados",
                        "domain": "ine.mx"
                    }
                ]
            }
        }
    }
    
    return mock_response
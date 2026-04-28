import logging
import re
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)

client = genai.Client(api_key=GEMINI_API_KEY)

def _extract_json(text: str) -> str:
    """
    Extrae el primer bloque JSON del texto de Gemini.
    Con google_search activo, Gemini puede devolver el JSON
    envuelto en markdown o precedido de texto explicativo.
    """
    if not text:
        return text

    # 1. Extraer bloque ```json ... ``` o ``` ... ```
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # 2. Extraer el primer objeto { ... } que aparezca en el texto
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0).strip()

    # 3. Si no encuentra nada, devolver el texto tal cual
    return text.strip()


def generate_response(prompt):
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        google_search=types.GoogleSearch()
                    )
                ],
            ),
        )

        raw_text = response.text
        logger.info(f"Respuesta cruda de Gemini (primeros 300 chars): {raw_text[:300]}")

        # Limpiar y extraer el JSON antes de devolver
        return _extract_json(raw_text)

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return '{"global_assessment":"Dudoso","fact_check_analysis":{"engine":"Gemini API","verdict":"No verificable","reasoning":"No se pudo generar una respuesta con Gemini.","references":[]}}'
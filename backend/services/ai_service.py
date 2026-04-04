import google.generativeai as genai
import logging
from config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)
genai.configure(api_key=GEMINI_API_KEY)

# model always return JSON
generation_config = genai.types.GenerationConfig(
    response_mime_type="application/json"
)

model = genai.GenerativeModel(
    GEMINI_MODEL,
    generation_config=generation_config
)

def generate_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return {"error": "Failed to generate response."}
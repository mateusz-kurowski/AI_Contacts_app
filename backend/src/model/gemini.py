import os
from google import genai
from google.genai import types
from src.config.config import model_config


API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY/GOOGLE_API_KEY environment variable")

google_client = genai.Client(
    api_key=API_KEY,
)

default_config = types.GenerateContentConfig(**model_config.model_client.model_dump())

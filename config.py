import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Cle API Groq manquante : verifie ton fichier .env")

EMBEDDING_MODEL = "distiluse-base-multilingual-cased-v2"
LLM_MODEL = "llama-3.3-70b-versatile"
CHROMA_DB_PATH = "./chroma_db"
CORPUS_JSON_PATH = "./data/corpus.json"
CORPUS_DATE = "2026-07-09"
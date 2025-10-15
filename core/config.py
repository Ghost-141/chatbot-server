from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

PRODUCTS_JSON_PATH = DATA_DIR / "product_info.json"
FAISS_DB_PATH = DATA_DIR / "db"

HUGGINGFACE_EMBEDDINGS_MODEL = "all-MiniLM-L6-v2"

GROQ_MODEL_NAME = "openai/gpt-oss-120b"
GROQ_TEMPERATURE = 0.3
GROQ_MAX_RETRIES = 3

RETRIEVER_SEARCH_TYPE = "mmr"
RETRIEVER_SEARCH_KWARGS = {"k": 5, "fetch_k": 50}

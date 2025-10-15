# Chatbot Server

Backend for a retrieval-augmented customer support chatbot that answers questions about products stored in `data/product_info.json`. The service exposes FastAPI endpoints for both conversational queries (powered by Groq + LangChain) and a catalog feed.

## Features

- Retrieval-augmented generation over the local product catalog.
- Groq LLM integration with retry, temperature, and prompt controls.
- FastAPI endpoints for chat responses and product listings.
- Pluggable service interfaces for chat and product backends.
- Automatic FAISS vector-store creation with caching for faster responses.

## Tech Stack

- Python 3.10+
- FastAPI & Uvicorn
- LangChain (Groq, Hugging Face embeddings, FAISS)
- Pydantic v2
- jq / JSONLoader for document parsing

## Getting Started

### 1. Clone & Environment

```bash
git clone <repo-url>
cd chatbot-server
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS/Linux
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -e .
# or: pip install -r pyproject.toml (using a PEP 621-aware installer like `uv`/`pip`)
```

### 3. Environment Variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=<your-groq-api-key>
```

> Never commit real API keys. The sample value in the repository is for development only.

### 4. Data Assets

- `data/product_info.json` - master product catalog.
- `data/db/` - FAISS vector index (auto-created on first run).

If you update the catalog, delete `data/db/` so the vector store can rebuild.

## Running the API

```bash
uvicorn main:app --reload
```

The app mounts its routers under:

- `POST /chat` - conversational answers.
- `GET /products` - product catalog snapshot.

Interactive docs: http://localhost:8000/docs

## API Reference

### `POST /chat`

- **Body** (`ChatQuery`):
  ```json
  {
    "message": "What discounts are available for the espresso machine?"
  }
  ```
- **Response** (`ChatResponse`):
  ```json
  {
    "message": "...LLM-generated answer..."
  }
  ```

### `GET /products`

- **Response** (`ProductList`):
  ```json
  {
    "products": [
      {
        "id": 1,
        "title": "Classic Coffee Maker",
        "description": "...",
        "category": "kitchen",
        "price": 99.99,
        "discountPercentage": 5.0,
        "rating": 4.5,
        "stock": 24,
        "tags": ["coffee", "appliance"],
        "brand": "BrewCo",
        "sku": "BC-1000",
        "weight": 3.2,
        "dimensions": {
          "width": 18.0,
          "height": 28.0,
          "depth": 20.0
        }
      }
    ],
    "total": 100,
    "skip": 0,
    "limit": 100
  }
  ```

## Project Layout

```
main.py                       # FastAPI application entrypoint
api/                          # Route definitions
  chat.py                     # /chat endpoint
  products.py                 # /products endpoint
core/
  config.py                   # Paths, model names, search params
  dependency.py               # Service dependency wiring
services/
  chatbot_service.py          # Chat pipeline orchestrator
  product_service.py          # JSON-backed product feed
  interface/                  # Abstract service contracts
models/schemas.py             # Pydantic request/response models
utils/groq_client.py          # LangChain + Groq utilities
system_prompts/prompt_v1.py   # Chatbot system prompt
data/                         # Product catalog and vector index
```

## Configuration Notes

Adjust defaults in `core/config.py`:

- `HUGGINGFACE_EMBEDDINGS_MODEL` to change embeddings.
- `GROQ_MODEL_NAME`, `GROQ_TEMPERATURE`, `GROQ_MAX_RETRIES` to tune LLM behavior.
- `RETRIEVER_SEARCH_*` to tweak vector-store retrieval.

## Troubleshooting

- **Missing API key**: ensure `.env` is present or set `GROQ_API_KEY` in the shell.
- **Vector store rebuilds every run**: confirm the process can write to `data/db/`.
- **LangChain import issues**: verify the versions pinned in `pyproject.toml` are installed.

## Next Steps

- Add automated tests around `ProductService` and `ChatService`.
- Integrate authentication or rate limiting if the API will be public.
- Implement error handling/logging middleware for better observability.

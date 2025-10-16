# Chatbot Server

FastAPI based backend for a retrieval-augmented customer support chatbot that answers questions about products stored in [`product_info.json`](data/product_info.json)
. The service exposes FastAPI endpoints for both conversational queries (powered by Groq + LangChain) and a catalog feed.

## Features

- Retrieval-augmented generation over the local product catalog.
- Groq LLM (**GPT-OSS-120B**) integration with retry, temperature, and custom prompt controls.
- FastAPI endpoints for chat responses and product listings.
- Added **logger** for easier debugging.
- Automatic **FAISS** vector-store creation with caching for faster responses.

## Tech Stack

- Python 3.10+
- FastAPI & Pydantic v2
- LangChain (Groq, Hugging Face embeddings, FAISS)
- jq and  JSONLoader for document parsing

## Getting Started

### 1. Clone & Environment

```bash
git clone https://github.com/Ghost-141/chatbot-server.git
cd chatbot-server
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS/Linux
```

### 2. Install Dependencies

- Install Using **pip:** 
  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

- Install Using **uv:**
  ```bash
  pip install --upgrade pip
  pip install uv 
  uv sync #automatically installs library
  ```

- Install Using **anaconda:**
  
  ```python
  conda create -n chatbot python=3.10
  conda activate chatbot
  pip install -r requirements.txt
  ```

### 3. Environment Variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=<your-groq-api-key>
```

## Running the Server

```bash
uvicorn main:app --reload #using pip/conda environment
uv run uvicorn main:app --reload #using uv 
```

### 4. Data Assets

- `data/product_info.json` - product catalog in `json` format.
- `data/db/` - FAISS vector index (auto-created on first run).

If you update the catalog, delete `data/db/` so the vector store can rebuild.



Interactive docs: http://localhost:8000/docs

## API Reference

### `POST /chat`

- **Body** (`ChatQuery`):
  ```json
  {
    "message": "Tell me more about kiwi."
  }
  ```
- **Response** (`ChatResponse`):
  ```json
  {
    "model_response": "Kiwi is a nutrient‑rich fruit that’s perfect for snacking or adding a tropical twist to dishes. It’s priced at **$2.49** and currently comes with a **15.22 % discount**. Customers rate it highly, with an average **rating of 4.93 / 5**. The item is **in stock** (99 units available) and ships **overnight**. Additionally, it includes a **6‑month warranty** for added peace of mind."
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

## Project Structure

```
.
├── api/
│   ├── chat.py
│   └── products.py
├── core/
│   ├── config.py
│   └── dependency.py
├── data/
│   ├── db
│   └── product_info.json
├── models/
│   └── schemas.py
├── servies/
│   ├── interface/
│   │   ├── chat_interface.py
│   │   └── product_interface.py
│   ├── chatbot_service.py
│   └── product_service.py  
├── system_prompts/
│   └── prompt_v1.py
├── utils/
│   └── groq_client.py
├── .env
├── requirements.txt
├── README.md
└── main.py
```

## Configuration Notes

Adjust defaults in `core/config.py`:

- `HUGGINGFACE_EMBEDDINGS_MODEL` to change embedding models.
- `GROQ_MODEL_NAME` to change LLM available in groq [website](https://console.groq.com/docs/models).
-  `GROQ_TEMPERATURE`, `GROQ_MAX_RETRIES` to tune LLM behavior.
- `RETRIEVER_SEARCH_*` to tweak vector-store retrieval.
- Use [uv](https://docs.astral.sh/uv/) for better user experience and avoid conflicts with other environments.



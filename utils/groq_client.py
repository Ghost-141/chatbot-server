import os
from functools import lru_cache
from typing import List, Optional, Sequence, Tuple

from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import JSONLoader

from core.config import (
    FAISS_DB_PATH,
    GROQ_MAX_RETRIES,
    GROQ_MODEL_NAME,
    GROQ_TEMPERATURE,
    HUGGINGFACE_EMBEDDINGS_MODEL,
    PRODUCTS_JSON_PATH,
    RETRIEVER_SEARCH_KWARGS,
    RETRIEVER_SEARCH_TYPE,
)
from system_prompts.prompt_v1 import prompt_v1


@lru_cache(maxsize=1)
def get_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not found in environment variables.")
    return api_key


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=HUGGINGFACE_EMBEDDINGS_MODEL)


def _load_documents() -> List:
    loader = JSONLoader(
        str(PRODUCTS_JSON_PATH),
        jq_schema=".products[]",
        text_content=False,
    )
    return loader.load()


def _build_vector_store() -> FAISS:
    documents = _load_documents()
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(documents, embeddings)
    try:
        vector_store.save_local(str(FAISS_DB_PATH))
    except OSError:
        # Persisting the index is an optimization; ignore if the environment is read-only.
        pass
    return vector_store


@lru_cache(maxsize=1)
def get_vector_store() -> FAISS:
    embeddings = get_embeddings()
    if FAISS_DB_PATH.exists():
        return FAISS.load_local(
            str(FAISS_DB_PATH),
            embeddings,
            allow_dangerous_deserialization=True,
        )
    return _build_vector_store()


@lru_cache(maxsize=1)
def get_retriever():
    return get_vector_store().as_retriever(
        search_type=RETRIEVER_SEARCH_TYPE,
        search_kwargs=RETRIEVER_SEARCH_KWARGS,
    )


@lru_cache(maxsize=1)
def get_prompt_template() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_v1,
    )


@lru_cache(maxsize=1)
def get_llm() -> ChatGroq:
    return ChatGroq(
        model=GROQ_MODEL_NAME,
        temperature=GROQ_TEMPERATURE,
        max_retries=GROQ_MAX_RETRIES,
        api_key=get_api_key(),
    )


def create_conversational_chain() -> ConversationalRetrievalChain:
    return ConversationalRetrievalChain.from_llm(
        llm=get_llm(),
        retriever=get_retriever(),
        combine_docs_chain_kwargs={"prompt": get_prompt_template()},
        return_source_documents=False,
    )


def run_chat_query(
    question: str,
    chat_history: Optional[Sequence[Tuple[str, str]]] = None,
) -> str:
    """Execute a question against the retrieval-augmented LLM pipeline."""
    if not question:
        raise ValueError("Question must be a non-empty string.")

    chain = create_conversational_chain()
    result = chain.invoke(
        {
            "question": question,
            "chat_history": list(chat_history or []),
        }
    )
    answer = result.get("answer")
    if answer is None:
        raise RuntimeError("LLM response did not include an answer field.")
    return answer

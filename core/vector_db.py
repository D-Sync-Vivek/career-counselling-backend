import os
import logging
from dotenv import load_dotenv

# LangChain Imports
from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()
logger = logging.getLogger(__name__)

# --- Configuration ---
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("CRITICAL: DATABASE_URL is missing in .env file.")

# Clean URL for psycopg2 (LangChain's PGVector requires this format)
DB_CONNECTION_STRING = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
if DB_CONNECTION_STRING.startswith("postgres://"):
    DB_CONNECTION_STRING = DB_CONNECTION_STRING.replace("postgres://", "postgresql+psycopg2://")

COLLECTION_NAME = "aptitude_questions"

# --- Lazy Loading Variables ---
_vector_store = None
_embeddings = None

def get_vector_store() -> PGVector:
    """
    Lazy loads the HuggingFace embeddings and connects to the PGVector database.
    This ensures the heavy embedding model only loads when an API actually needs it.
    """
    global _vector_store, _embeddings
    
    if _vector_store is None:
        logger.info("Lazy Loading Embedding Model & Connecting to Vector Store...")
        
        # 1. Initialize Embeddings
        _embeddings = HuggingFaceEmbeddings(
            model_name="intfloat/multilingual-e5-small",
            model_kwargs={'device': 'cpu'}, 
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # 2. Initialize Vector Store
        _vector_store = PGVector(
            connection_string=DB_CONNECTION_STRING,
            embedding_function=_embeddings,
            collection_name=COLLECTION_NAME,
            use_jsonb=True,
            engine_args={"pool_pre_ping": True} # Prevents Neon connection drops
        )
        logger.info("Vector Store Initialized Successfully!")
        
    return _vector_store
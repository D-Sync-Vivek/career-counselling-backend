import os
import tempfile
import logging
from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends
from pydantic import BaseModel
import psycopg2 # Required if you use the reset-topic route

# LangChain Imports
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import PGVector

# Import the lazy-loaded vector store from main
from core.vector_db import get_vector_store

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Ingestion"])

# --- Pydantic Models ---
class IngestionResponse(BaseModel):
    message: str
    chunks_processed: int
    metadata: dict

# --- CORE ROUTE ---
@router.post("/ingest/aptitude", response_model=IngestionResponse)
async def ingest_aptitude_pdf(
    file: UploadFile = File(...),
    category: str = Form(..., description="e.g., Quantitative Aptitude, Logical Reasoning"),
    topic: str = Form(..., description="e.g., Time and Work, Profit and Loss"),
    target_grade: str = Form(..., description="e.g., 6-8, 9-10, 11-12"),     # <-- NEW
    difficulty: str = Form(..., description="e.g., Easy, Medium, Hard"),       # <-- NEW
    vs: PGVector = Depends(get_vector_store)
):
    """ Uploads an Aptitude PDF, chunks it, and saves it with rich metadata to the PostgreSQL Vector Database. """
    logger.info(f"Starting ingestion for Category: {category}, Topic: {topic}, Grade: {target_grade}, Difficulty: {difficulty}")
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDFs supported.")

    try:
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File error: {str(e)}")

    try:
        logger.info("Parsing PDF document...")
        loader = PyMuPDFLoader(tmp_path)
        documents = loader.load()

        logger.info("Chunking document text...")
        # Chunk size of 1000 is good for keeping 2-3 aptitude questions together
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        chunks = text_splitter.split_documents(documents)

        # Injecting our rich custom metadata into every single chunk
        for chunk in chunks:
            chunk.metadata.update({
                "category": category,
                "topic": topic,
                "target_grade": target_grade, # <-- NEW
                "difficulty": difficulty      # <-- NEW
            })

        logger.info(f"Inserting {len(chunks)} vectors into PostgreSQL...")
        vs.add_documents(chunks)
        logger.info("Vector insertion complete!")

    except Exception as e:
        logger.error(f"Error during document processing: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return IngestionResponse(
        message="PDF successfully ingested and vectorized.",
        chunks_processed=len(chunks),
        metadata={
            "category": category, 
            "topic": topic, 
            "target_grade": target_grade, 
            "difficulty": difficulty
        }
    )

# --- TARGETED DELETE ROUTE (Optional but highly recommended) ---
@router.delete("/reset-topic")
async def delete_topic_vectors(
    category: str, 
    topic: str,
    target_grade: str,
    difficulty: str
):
    """ Deletes specific vectors matching exact metadata from the database. """
    logger.info(f"Attempting to delete vectors for {topic} ({difficulty}, Grade {target_grade})")
    
    db_url = os.getenv("DATABASE_URL")
    
    try:
        clean_url = db_url.replace("postgresql+psycopg2://", "postgresql://")
        conn = psycopg2.connect(clean_url)
        cursor = conn.cursor()

        # SQL query to delete based on the JSON metadata keys
        delete_query = """
            DELETE FROM langchain_pg_embedding 
            WHERE cmetadata->>'category' = %s 
            AND cmetadata->>'topic' = %s
            AND cmetadata->>'target_grade' = %s
            AND cmetadata->>'difficulty' = %s;
        """
        
        cursor.execute(delete_query, (category, topic, target_grade, difficulty))
        deleted_count = cursor.rowcount
        
        conn.commit()
        cursor.close()
        conn.close()

        logger.info(f"Successfully deleted {deleted_count} chunks.")
        
        return {
            "message": "Vectors deleted successfully.",
            "chunks_removed": deleted_count
        }

    except Exception as e:
        logger.error(f"Failed to delete vectors: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
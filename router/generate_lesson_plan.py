import os
import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List

# LangChain Imports
from langchain_community.vectorstores import PGVector
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# Import the lazy-loaded vector store from main
from main import get_vector_store

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Quiz Generation"])

# --- Pydantic Models for Structured AI Output ---
class AptitudeMCQ(BaseModel):
    question: str = Field(description="The mathematical or logical aptitude question")
    options: List[str] = Field(description="Exactly 4 distinct options for the MCQ")
    correct_answer: str = Field(description="The exact text of the correct option")
    explanation: str = Field(description="A step-by-step mathematical breakdown of how to solve the problem")

class AptitudeQuizOutput(BaseModel):
    quiz_summary: str = Field(description="A 1-2 sentence overview of the concepts covered in this quiz")
    questions: List[AptitudeMCQ] = Field(description="A list of multiple choice questions")

# --- Endpoints ---
@router.post("/generate_quiz", response_model=AptitudeQuizOutput)
async def generate_aptitude_quiz(
    category: str, 
    topic: str, 
    target_grade: str, # <-- NEW: Adaptive input
    difficulty: str,   # <-- NEW: Adaptive input
    num_questions: int = 5,
    vs: PGVector = Depends(get_vector_store)
):
    """ Retrieves context from Postgres and generates a structured, grade-appropriate aptitude quiz. """
    logger.info(f"Generating {num_questions} {difficulty} questions for Grade {target_grade} on {topic}")

    # 1. Vector Search (RAG) - Strict Filtering
    try:
        retriever = vs.as_retriever(
            search_kwargs={
                "k": 15, 
                "filter": {
                    "category": category,
                    "topic": topic,
                    "target_grade": target_grade, # <-- NEW: Only pull age-appropriate chunks
                    "difficulty": difficulty      # <-- NEW: Only pull correct difficulty chunks
                }
            }
        )

        # Ask the vector DB to find chunks matching the specific difficulty
        docs = retriever.invoke(f"Extract {difficulty} aptitude problems for grade {target_grade} regarding {topic}")
        context_text = "\n\n".join([doc.page_content for doc in docs])

        if not context_text:
            logger.warning("No context found in PostgreSQL for the given filters.")
            raise HTTPException(status_code=404, detail="No ingested data found matching this specific grade and difficulty.")
        
        logger.info(f"Successfully retrieved {len(docs)} chunks from the database.")
    except Exception as e:
        logger.error(f"Database retrieval failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database retrieval failed.")

    # 2. Initialize DeepSeek API
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_api_key:
        raise HTTPException(status_code=500, detail="CRITICAL: DEEPSEEK_API_KEY is missing in .env file.")
    
    llm = ChatOpenAI(
        model="deepseek-chat", 
        api_key=deepseek_api_key, 
        base_url="https://api.deepseek.com",
        temperature=0.3 
    )

    # 3. Setup the Pydantic Output Parser
    parser = PydanticOutputParser(pydantic_object=AptitudeQuizOutput)

    # 4. Create the Prompt (Updated to enforce grade-level language)
    system_prompt = """
    You are an expert educational assessor. 
    Your task is to generate a structured Aptitude Quiz based strictly on the provided context.
    
    CRITICAL CONSTRAINTS:
    - Target Audience: Grade {target_grade} student. The language and mathematical complexity MUST be appropriate for this age group.
    - Difficulty Level: {difficulty}. Ensure the problems match this specific difficulty level.
    - Generate EXACTLY {num_questions} Multiple Choice Questions (MCQs).
    - Provide a clear, step-by-step mathematical explanation for the correct answer tailored to a Grade {target_grade} reading level.
    - Do not hallucinate formulas; use the logic presented in the context.
    
    {format_instructions}
    
    Context from Vector Database:
    {context}
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Generate a {difficulty} aptitude quiz for Grade {target_grade} on Category: {category}, Topic: {topic}.")
    ])

    # 5. Execute the Chain (Prompt -> LLM -> Parser)
    logger.info("Sending prompt and context to DeepSeek API...")
    chain = prompt | llm | parser
    
    try:
        result = chain.invoke({
            "context": context_text,
            "category": category,
            "topic": topic,
            "target_grade": target_grade,
            "difficulty": difficulty,
            "num_questions": num_questions,
            "format_instructions": parser.get_format_instructions()
        })
        logger.info("Successfully generated and parsed JSON from DeepSeek.")
        return result
    except Exception as e:
        logger.error(f"LLM Generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"LLM Generation failed: {str(e)}")
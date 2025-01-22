from fastapi import FastAPI, UploadFile, HTTPException, File, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict
from dotenv import load_dotenv
import fitz  # PyMuPDF
import os
import uuid
import sqlite3
import asyncio
import logging
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from contextlib import contextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='/tmp/app.log'  # Updated to write logs to /tmp folder
)
logger = logging.getLogger(__name__)

# Load environment variables
logger.info("Loading environment variables...")
load_dotenv()

# Environment Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    logger.error("ANTHROPIC_API_KEY not found in environment variables")
    raise ValueError("ANTHROPIC_API_KEY is not set in the environment or .env file.")

# Constants
UPLOAD_DIR = "uploaded_files"
DB_PATH = "documents.db"
ALLOWED_FILE_TYPES = [".pdf"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
CHUNK_SIZE = 4096  # Chunk size for file reading

# Make Anthropic client global
anthropic_client = None

def initialize_anthropic():
    """Initialize the Anthropic client globally."""
    global anthropic_client
    try:
        logger.info("Initializing Anthropic client...")
        anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
        logger.info("Anthropic client initialized successfully")
    except Exception as e:
        logger.error(f"Anthropic client initialization error: {str(e)}")
        raise ValueError(f"Failed to initialize Anthropic client: {str(e)}")

# Initialize Anthropic client
initialize_anthropic()

# FastAPI app setup
app = FastAPI(
    title="PDF Question Answering System",
    description="API for uploading PDFs and asking questions about their content",
    version="1.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS setup
origins = [
    "https://your-vercel-frontend-url.vercel.app",  # Production
    "http://localhost:3000",  # Local development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Enhanced Models
class QuestionRequest(BaseModel):
    document_id: str = Field(..., description="Unique identifier of the document")
    question: str = Field(..., min_length=1, max_length=1000, description="Question to ask about the document")

class DocumentResponse(BaseModel):
    id: str
    filename: str
    upload_date: str
    message: str
    file_size: int = Field(..., description="Size of the file in bytes")

class DocumentInfo(BaseModel):
    id: str
    filename: str
    upload_date: str
    file_size: int
    page_count: Optional[int] = Field(None, description="Number of pages in the PDF")

# Context manager for database connections
@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        yield conn
    finally:
        if conn:
            conn.close()

# Enhanced database initialization
def initialize_db():
    """Initialize database with corrected schema"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Drop existing table if it exists
            cursor.execute("DROP TABLE IF EXISTS documents")
            
            # Create table with all required columns
            cursor.execute("""
                CREATE TABLE documents (
                    id TEXT PRIMARY KEY,
                    filename TEXT NOT NULL,
                    upload_date TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    text_content TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    page_count INTEGER,
                    last_accessed TEXT
                )
            """)
            conn.commit()
        logger.info("Database initialized successfully with corrected schema")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise

# Initialize database
initialize_db()

# Enhanced utility functions
async def extract_text_from_pdf(file_path: str) -> tuple[str, int]:
    """Extract text from PDF and return text content and page count."""
    try:
        doc = fitz.open(file_path)
        text = ""
        page_count = doc.page_count
        
        for page in doc:
            text += page.get_text()
        doc.close()
        return text, page_count
    except Exception as e:
        logger.error(f"PDF text extraction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting text from PDF: {str(e)}"
        )

def validate_file(file: UploadFile) -> None:
    """Enhanced file validation with detailed checks."""
    file_extension = os.path.splitext(file.filename)[1].lower()
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    if file_extension not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Only {', '.join(ALLOWED_FILE_TYPES)} files are allowed"
        )

async def get_claude_response(question: str, context: str) -> str:
    """Get response from Claude for a given question and context."""
    try:
        prompt = f"{HUMAN_PROMPT}Context: {context}\n\nQuestion: {question}\n\nPlease answer the question based on the context provided above.{AI_PROMPT}"
        
        message = await anthropic_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return message.content[0].text
        
    except Exception as e:
        logger.error(f"Claude API error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting response from Claude: {str(e)}"
        )

# Enhanced API Endpoints
@app.get("/")
async def root():
    """Enhanced health check endpoint."""
    return {
        "status": "OK",
        "message": "PDF QA System API is running",
        "version": app.version,
        "api_key_configured": bool(ANTHROPIC_API_KEY),
        "upload_dir_exists": os.path.exists(UPLOAD_DIR),
        "database_exists": os.path.exists(DB_PATH)
    }

@app.post("/upload", response_model=DocumentResponse)
async def upload_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Enhanced PDF upload endpoint with background processing."""
    try:
        validate_file(file)
        content = await file.read()
        file_size = len(content)
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum limit of {MAX_FILE_SIZE/1024/1024}MB"
            )
        
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        text_content, page_count = await extract_text_from_pdf(file_path)
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO documents (
                    id, filename, upload_date, file_path, text_content, 
                    file_size, page_count, last_accessed
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (file_id, file.filename, datetime.now().isoformat(), 
                 file_path, text_content, file_size, page_count, 
                 datetime.now().isoformat())
            )
            conn.commit()
        
        return DocumentResponse(
            id=file_id,
            filename=file.filename,
            upload_date=datetime.now().isoformat(),
            message="File uploaded successfully",
            file_size=file_size
        )
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Enhanced question answering endpoint with improved error handling."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT text_content, filename
                FROM documents 
                WHERE id = ?
                """,
                (request.document_id,)
            )
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(status_code=404, detail="Document not found")
            
            text_content = result['text_content']
            filename = result['filename']
            
            # Update last accessed timestamp
            cursor.execute(
                "UPDATE documents SET last_accessed = ? WHERE id = ?",
                (datetime.now().isoformat(), request.document_id)
            )
            conn.commit()
        
        answer = await get_claude_response(request.question, text_content)
        
        return {
            "answer": answer,
            "document": filename,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Ask question error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Run app locally (in development environment)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

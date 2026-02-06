from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routes import tasks
from routes import chat
from db import engine
from models import Task
try:
    from mcp_server import mcp_server
except Exception as e:
    # Handle any unexpected errors during import
    import logging
    logging.warning(f"Could not import mcp_server: {e}")
    mcp_server = None

app = FastAPI(title="Todo API", version="1.0.0")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Not found"}
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hackathon-ii-phase-iii-todo-full-stack-web-applicati-377xbdnbb.vercel.app",  # Production frontend
        "https://nishanazar-new-repo.hf.space",  # Hugging Face Space for backend
        "http://localhost:3000",  # Local development frontend
        "http://localhost:3001",  # Alternative local development frontend
        "http://localhost:3003",  # Alternative local development frontend (Next.js default when 3000/3001/3002 are taken)
        "http://127.0.0.1:3000",  # Alternative localhost for frontend
        "http://127.0.0.1:3003",  # Alternative localhost for frontend
        "http://localhost:8000",  # Allow requests from same origin (for development)
        "http://127.0.0.1:8000",  # Allow requests from same origin (for development)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicitly allow these methods
    allow_headers=["*"],  # Allow all headers
    # Allow preflight requests to bypass auth
    allow_origin_regex=r"https?://localhost(:[0-9]+)?|https?://127\.0\.0\.1(:[0-9]+)?",
)

# Create the database tables
@app.on_event("startup")
def on_startup():
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

# Include the task routes
app.include_router(tasks.router, prefix="/api/{user_id}", tags=["tasks"])

# Include the chat routes
app.include_router(chat.router, prefix="/api/{user_id}", tags=["chat"])

# Mount the MCP server at /mcp if it's available
if mcp_server is not None:
    app.mount("/mcp", mcp_server)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
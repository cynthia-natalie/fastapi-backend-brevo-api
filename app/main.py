from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from app.api import router
from app.logger import logger

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="FastAPI Secure API", version="1.0")

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# CORS Middleware - Restrict origins for better security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"], # Change this to your actual frontend domain 
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["X-API-KEY"],
)

app.include_router(router)

@app.get("/")
def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "ok", "message": "FastAPI service is running"}
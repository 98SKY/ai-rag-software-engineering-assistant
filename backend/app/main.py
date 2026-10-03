import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models  # noqa: F401
from app.api.v1 import api_router
from app.core.database import Base, engine


load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI RAG Software Engineering Assistant",
    description="M.Tech AI Project using Retrieval-Augmented Generation",
    version="1.0.0",
)

frontend_url = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173",
)

allowed_origins = [
    "http://localhost:5173",
]

if frontend_url not in allowed_origins:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_router,
    prefix="/api/v1",
)


@app.get("/")
async def root():
    return {
        "message": "AI RAG Software Engineering Assistant API"
    }
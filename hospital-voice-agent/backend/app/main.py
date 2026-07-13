from fastapi import FastAPI
from app.database.database import Base, engine
import app.database
from app.api.routes import router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Hospital Voice Agent",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "Hospital Voice Agent API Running"
    }
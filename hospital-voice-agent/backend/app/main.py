from fastapi import FastAPI
from app.database.database import Base, engine
import app.database
from app.api.routes import router



app = FastAPI(
    title="AI Hospital Voice Agent",
)

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Hospital Voice Agent API Running"
    }
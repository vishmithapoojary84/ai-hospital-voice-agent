from fastapi import FastAPI

app = FastAPI(
    title="Hospital Voice Agent API",
    description="Backend API for Hospital Voice Agent",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hospital Voice Agent API"}

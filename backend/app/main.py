from fastapi import FastAPI

app = FastAPI(
    title="NeuroOne API",
    version="1.0.0",
    description="Backend API for NeuroOne"
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to NeuroOne API"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
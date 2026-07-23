import uvicorn
from fastapi import FastAPI
from sqlalchemy import text

from app.api.router import api_router
from app.core.config import settings
from app.core.database import engine

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for NeuroOne",
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}"}


from sqlalchemy import text
from app.core.database import engine

@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"database": "connected"}
    except Exception as e:
        return {"database": "error", "details": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
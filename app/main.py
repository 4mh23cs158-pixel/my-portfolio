from fastapi import FastAPI

app = FastAPI(
    title="My Portfolio API",
    description="Backend API for my personal portfolio",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Portfolio Backend is running!"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy"
    }
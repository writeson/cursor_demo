"""
Entry point for the FastAPI application.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("project.src.main:app", host="0.0.0.0", port=8000, reload=True)
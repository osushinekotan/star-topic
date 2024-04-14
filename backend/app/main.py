from fastapi import FastAPI

from .routers import github

app = FastAPI(title="GitHub Repository Analysis API")

app.include_router(github.router, prefix="/github", tags=["GitHub"])

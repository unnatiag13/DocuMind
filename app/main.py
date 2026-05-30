from .auth.router import router as auth_router
from .documents.router import router as doc_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(auth_router,prefix="/auth")
app.include_router(doc_router,prefix="/documents")
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .routers import boletins

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BU Parser API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(boletins.router)

FRONTEND_DIR = os.getenv(
    "FRONTEND_DIR", os.path.join(os.path.dirname(__file__), "..", "frontend")
)


@app.get("/", include_in_schema=False)
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# Serve o restante de arquivos estáticos do frontend (se houver: css, js, imagens...).
# A rota "/" definida acima tem prioridade sobre este mount.
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

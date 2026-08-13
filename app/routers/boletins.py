import hashlib
import os

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import DATA_DIR, get_db

router = APIRouter(prefix="/api/boletins", tags=["boletins"])

UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=schemas.BoletimOut)
async def upload_boletim(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos.")

    conteudo = await file.read()
    if not conteudo:
        raise HTTPException(status_code=400, detail="Arquivo vazio.")

    sha256 = hashlib.sha256(conteudo).hexdigest()

    # Se o mesmo arquivo (mesmo hash) já foi enviado antes, apenas retorna o registro existente.
    existente = db.query(models.Boletim).filter(models.Boletim.sha256 == sha256).first()
    if existente:
        return existente

    caminho_destino = os.path.join(UPLOAD_DIR, f"{sha256}.pdf")
    with open(caminho_destino, "wb") as f:
        f.write(conteudo)

    boletim = models.Boletim(
        nome_arquivo=file.filename,
        sha256=sha256,
        status="recebido",
    )
    db.add(boletim)
    try:
        db.commit()
    except IntegrityError:
        # Corrida entre duas requisições com o mesmo hash: retorna o já existente.
        db.rollback()
        return db.query(models.Boletim).filter(models.Boletim.sha256 == sha256).first()

    db.refresh(boletim)
    return boletim


@router.get("", response_model=list[schemas.BoletimOut])
def listar_boletins(db: Session = Depends(get_db)):
    return db.query(models.Boletim).order_by(models.Boletim.id.desc()).all()

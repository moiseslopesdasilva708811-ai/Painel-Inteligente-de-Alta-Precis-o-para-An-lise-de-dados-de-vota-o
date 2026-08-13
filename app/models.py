from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .database import Base


class Boletim(Base):
    __tablename__ = "boletins"

    id = Column(Integer, primary_key=True, index=True)
    nome_arquivo = Column(String, nullable=False)
    sha256 = Column(String(64), nullable=False, unique=True, index=True)
    status = Column(String, nullable=False, default="recebido")
    data_processamento = Column(DateTime, default=datetime.utcnow, nullable=False)

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BoletimOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome_arquivo: str
    sha256: str
    status: str
    data_processamento: datetime

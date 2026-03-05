from pydantic import BaseModel
from typing import List

class ConfiguracaoSistema(BaseModel):
    unidades_medida: List[str] = []

class BackupResponse(BaseModel):
    status: str
    message: str
    timestamp: str
    file_url: str | None = None

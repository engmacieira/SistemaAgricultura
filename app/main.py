from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging_config import setup_logging

# Inicialização do logging
setup_logging()

# Importando os routers
from app.presentation.routers import (
    produtores,
    servicos,
    execucoes,
    pagamentos,
    usuarios,
    logs,
    administrador,
    dashboard,
    relatorios
)

app = FastAPI(
    title="Serviços Agrícolas API",
    description="API para o sistema de gestão de serviços agrícolas.",
    version="1.0.0"
)

# Startup Backup
@app.on_event("startup")
async def startup_event():
    from app.infrastructure.services.backup_service import BackupService
    backup_service = BackupService()
    try:
        backup_service.create_backup()
        backup_service.clean_old_backups(days=10)
    except Exception as e:
        print(f"Erro no backup automático inicial: {e}")

# Configuração de CORS (permitindo o frontend se conectar)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrando os routers
app.include_router(produtores.router)
app.include_router(servicos.router)
app.include_router(execucoes.router)
app.include_router(pagamentos.router)
app.include_router(usuarios.router)
app.include_router(logs.router)
app.include_router(administrador.router)
app.include_router(dashboard.router)
app.include_router(relatorios.router)

@app.get("/")
def root():
    return {"message": "Bem-vindo à API de Serviços Agrícolas"}

from fastapi import FastAPI, Request
import time
import logging      
from app.core.logging_config import setup_logging
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging_config import setup_logging
from contextlib import asynccontextmanager
from app.core.database import Base, engine, SQLALCHEMY_DATABASE_URL
from alembic.config import Config
from alembic import command
import os

setup_logging()

# Inicialização do logging
acesso_logger = logging.getLogger("sistema.acesso")

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
    relatorios,
    solicitacoes
)

def run_migrations():
    # Encontra o diretório raiz do projeto (funciona tanto em dev quanto compilado pelo Nuitka)
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    alembic_ini_path = os.path.join(base_path, "alembic.ini")
    
    if os.path.exists(alembic_ini_path):
        try:
            print("Executando migrações do banco de dados via Alembic...")
            alembic_cfg = Config(alembic_ini_path)
            # Garante que vai usar a URL apontada pro AppData
            alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
            alembic_cfg.set_main_option("script_location", os.path.join(base_path, "alembic"))
            command.upgrade(alembic_cfg, "head")
            print("Migrações concluídas com sucesso!")
        except Exception as e:
            print(f"Aviso no Alembic: {e}. Gerando as tabelas com fallback...")
            Base.metadata.create_all(bind=engine)
    else:
        print("alembic.ini não encontrado. Gerando tabelas via SQLAlchemy (Fallback Nuitka)...")
        Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Gera/Atualiza as tabelas do banco de dados local da máquina
    run_migrations()

    # 2. --- DÍVIDA TÉCNICA RESOLVIDA: SEED DO CLIENTE FINAL ---
    # Garante que o usuário Master existe logo no primeiro segundo de vida do app
    from app.scripts.create_master_admin import create_master_admin
    try:
        print("Verificando credenciais do Master Admin...")
        create_master_admin()
    except Exception as e:
        print(f"Aviso: Não foi possível rodar o seed do admin: {e}")
    # ----------------------------------------------------------

    # 3. Startup Backup
    from app.infrastructure.services.backup_service import BackupService
    backup_service = BackupService()
    try:
        backup_service.create_backup()
        backup_service.clean_old_backups(days=10)
    except Exception as e:
        print(f"Erro no backup automático inicial: {e}")
    yield

app = FastAPI(
    title="Serviços Agrícolas API",
    description="API para o sistema de gestão de serviços agrícolas.",
    version="1.0.0",
    lifespan=lifespan
)

@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    start_time = time.time()
    
    # Processa a requisição e gera a resposta
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # Filtro de Arquiteto: Ignoramos os arquivos .js e .css do React para não poluir o log,
    # focando apenas nas chamadas da API e navegação principal.
    if not request.url.path.startswith("/assets"):
        acesso_logger.info(f"[{request.method}] {request.url.path} - Status: {response.status_code} - Tempo: {process_time:.4f}s")
        
    return response

# Configuração de CORS (permitindo o frontend se conectar)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",   # Adicionado para a versão desktop
    "http://127.0.0.1:8000",   # Adicionado para a versão desktop
    "http://localhost:5173", # Adicionado para o Vite Dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criando um roteador central para o prefixo /api (Padronizado)
from fastapi import APIRouter
api_router = APIRouter(prefix="/api")
api_router.include_router(produtores.router)
api_router.include_router(servicos.router)
api_router.include_router(execucoes.router)
api_router.include_router(pagamentos.router)
api_router.include_router(usuarios.router)
api_router.include_router(logs.router)
api_router.include_router(administrador.router)
api_router.include_router(dashboard.router)
api_router.include_router(relatorios.router)
api_router.include_router(solicitacoes.router)

# Registrando os routers na raiz e no prefixo /api para compatibilidade
app.include_router(api_router)

# Fallback para rotas sem prefixo (se necessário, ou manter apenas /api)
# Para manter a estrutura anterior onde funcionava sem /api também:
app.include_router(produtores.router)
app.include_router(servicos.router)
app.include_router(execucoes.router)
app.include_router(pagamentos.router)
app.include_router(usuarios.router)
app.include_router(logs.router)
app.include_router(administrador.router)
app.include_router(dashboard.router)
app.include_router(relatorios.router)

@app.get("/api")
def root():
    return {"message": "Bem-vindo à API de Serviços Agrícolas"}

# Lógica do SPA Middleware e Static Files
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request

frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
frontend_assets = os.path.join(frontend_dist, "assets")

if os.path.isdir(frontend_assets):
    app.mount("/assets", StaticFiles(directory=frontend_assets), name="assets")

@app.middleware("http")
async def spa_middleware(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404 and request.method == "GET":
        if request.url.path.startswith("/api/"):
            return response
        path = request.url.path.lstrip("/")
        if path:
            file_path = os.path.join(frontend_dist, path)
            if os.path.isfile(file_path):
                return FileResponse(file_path)
        accept = request.headers.get("accept", "")
        if "text/html" in accept or "." not in path:
            index_file = os.path.join(frontend_dist, "index.html")
            if os.path.isfile(index_file):
                return FileResponse(index_file)
    return response



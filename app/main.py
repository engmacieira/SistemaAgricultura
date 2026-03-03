from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importando os routers
from app.presentation.routers import (
    produtores,
    servicos,
    execucoes,
    pagamentos,
    usuarios,
    logs,
    administrador
)

app = FastAPI(
    title="Serviços Agrícolas API",
    description="API para o sistema de gestão de serviços agrícolas.",
    version="1.0.0"
)

# Configuração de CORS (permitindo o frontend se conectar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.get("/")
def root():
    return {"message": "Bem-vindo à API de Serviços Agrícolas"}

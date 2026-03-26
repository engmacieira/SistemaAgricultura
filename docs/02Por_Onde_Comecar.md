# 🚀 Manual de Início Rápido: Sistema Agricultura

Bem-vindo ao projeto! Este guia é um resumo da situação atual do projeto e quais os passos a seguir.

## 📍 Estado Atual da Missão
* **Fase do Projeto:** Refatoração de MVP após feedback de campo (Mudança de Domínio).
* **Sprint Atual:** Sprint 01 - Refatoração do Fluxo de Ordem de Serviço (Fila de Espera -> Execução).
* **Última Ação Realizada:** Atualização das User Stories e criação do Sprint Backlog (Documentação de escopo).
* **PRÓXIMO PASSO IMEDIATO:** **Backend (Database)**. O desenvolvedor deve analisar os ficheiros atuais em `app/models/` (especificamente os modelos de Agendamento/Execução e Pagamento) e preparar as classes SQLAlchemy para a nova modelagem de Ordem de Serviço, seguida da criação da **migration no Alembic**.

## 🏗️ Definições Arquiteturais (Não Quebrar)
* **Backend:** Python (FastAPI) + SQLAlchemy + Alembic.
    * *Regra:* Repositories com tratamento de erro `try/except` obrigatório.
    * *Banco:* SQLite (Local/Nuitka).
* **Segurança Local:** Backup do `.db` necessário, `.env` para segredos.
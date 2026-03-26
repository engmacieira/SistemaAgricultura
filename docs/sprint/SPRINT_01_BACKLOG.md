# 🗺️ Sprint 01: Refatoração do Fluxo de Ordem de Serviço

**Objetivo:** Alterar a lógica de "Agendamento com hora marcada" para "Fila de Espera -> Execução -> Pagamento" e mitigar vulnerabilidades locais.
**Status:** Em Execução
**Tecnologia Principal:** FastAPI / SQLAlchemy / Alembic / React

---

## 🎯 Backlog de Funcionalidades (Escopo)
* **[US-01]** Registar Solicitação na Fila de Espera
* **[US-02]** Registar a Execução do Serviço (Dar Baixa)
* **[US-03]** Processar Pagamento da Execução

---

## 🛠️ Plano Técnico de Execução

1.  **Setup/Infra (Segurança Local):** Criar rotina de backup automático do SQLite (`.db`) e isolar chaves secretas do JWT em variáveis de ambiente.
2.  **Database (Alembic):** * Criar migration para alterar/criar a tabela `Solicitacao` (Fila de espera, sem data/hora de fim rígida).
    * Criar/Alterar tabela `Execucao` (Horas reais, valor_unitario, valor_total, FK_Solicitacao).
    * Ajustar tabela `Pagamento` para referenciar `Execucao`.
3.  **Backend (FastAPI):** Refatorar os repositórios (`execucao_repository`, `pagamento_repository`) e rotas para refletir as novas entidades. Manter o padrão de tratamento de erros com `try/except`.
4.  **Frontend (React):** * Substituir o ecrã de "Calendário" por uma view de "Kanban" ou Lista de Fila de Espera.
    * Criar o Modal de "Baixa de Execução" acoplado ao cartão da Fila de Espera.

---

## 📝 Definição de Pronto (DoD)
* [ ] Tabelas atualizadas via Alembic sem perda de dados (se houver dados úteis).
* [ ] CRUD de Execução a funcionar e a calcular o valor total com base nas horas reais.
* [ ] Front-end a consumir a nova estrutura sem quebrar.
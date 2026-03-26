# 🗺️ Mapeamento de User Stories - Sistema Agricultura

**Visão do Produto:** Uma plataforma local para gestão de serviços agrícolas, focada em filas de espera, execução real em campo e faturação precisa, operando de forma offline.

---

## 📍 Backlog Funcional (Refatoração: Fluxo de Ordem de Serviço)

### 📦 Módulo 1: Fila de Espera (Solicitações)
*O produtor solicita um serviço, mas a execução depende da disponibilidade e ordem da fila.*

* **[US-01] Registar Solicitação na Fila de Espera**
    * **Como:** Operador do Sistema.
    * **Eu quero:** Adicionar um produtor e a sua necessidade (ex: "precisa de trator") a uma fila de espera, sem definir horas exatas.
    * **Para que:** O serviço fique pendente e visível para a equipa de campo.
    * **Regra de Negócio:** O estado inicial deve ser `PENDENTE`. Não requer validação de conflito de horários.

### 🔧 Módulo 2: Execução em Campo (Ordem de Serviço)
*O trabalho real feito na fazenda, que dita o custo final.*

* **[US-02] Registar a Execução do Serviço (Dar Baixa)**
    * **Como:** Operador do Sistema.
    * **Eu quero:** Vincular uma "Execução" a uma "Solicitação", informando os dados reais (serviço prestado, horas gastas, maquinaria utilizada, valor por hora do dia).
    * **Para que:** O sistema calcule o valor exato a ser cobrado.
    * **Regra de Negócio:** A Execução é que gera o valor financeiro. Ao registar a execução, a solicitação original muda para `CONCLUIDO`.

### 💰 Módulo 3: Faturação e Pagamentos
* **[US-03] Processar Pagamento da Execução**
    * **Como:** Operador do Sistema.
    * **Eu quero:** Registar o pagamento com base no valor final da Execução (e não da solicitação inicial).
    * **Para que:** O caixa reflita a realidade do trabalho feito.
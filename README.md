# 🏦 Ledger API - Sistema financeiro simples com alta integrídade

API REST de "Mini-Contabilidade" desenvolvida para garantir consistência financeira absoluta em ambientes de alta concorrência. 

O projeto simula o núcleo de uma carteira digital, focando em **Atomicidade, Consistência, Isolamento e Durabilidade (ACID)**.

## 🚀 Tecnologias e Decisões Arquiteturais

* **Python 3.13+ & FastAPI**: Alta performance com `async/await`.
* **SQL Server 2022**: Banco relacional robusto para integridade de dados.
* **SQLAlchemy (Async)**: ORM moderno utilizando o driver `aioodbc` para operações não bloqueantes.
* **Pydantic**: Validação rigorosa de schemas de entrada e saída.
* **Docker & Docker Compose**: Ambiente de desenvolvimento isolado e reprodutível.

## 🧠 Diferenciais Técnicos

### 1. Integridade ACID & Concorrência
Diferente de sistemas comuns que validam saldo apenas na memória, este projeto utiliza **pessimistic Locking** (`with_for_update`) no banco de dados.
* Isso impede *race conditions* (duas transferências simultâneas gastarem o mesmo saldo).
* Se a API cair no meio da operação, o SQL Server garante o **rollback** automático.

### 2. Extrato via Window Functions
O cálculo de saldo histórico ("saldo após a transação") não é feito via loop no Python (O(n)), mas sim utilizando **Window Functions** do SQL Server (`SUM() OVER()`). Isso garante performance extrema mesmo com milhões de linhas.

### 3. Constraints Nativas
Regras de negócio críticas (como "saldo não pode ser negativo") são garantidas por `CHECK CONSTRAINTS` no banco de dados, servindo como última linha de defesa.

## 🛠️ Como Rodar

### Pré-requisitos
* Docker & Docker Compose
* Gerenciador de pacotes `uv` (ou pip)

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/levi-paz/ledger-api.git](https://github.com/levi-paz/ledger-api.git)
   cd ledger-api
   ```

2. **Suba o banco de dados:**
    ```bash
    docker compose up -d
    ```

3. **Configure o ambiente do seu arquivo ```.env``` na pasta raiz do projeto:**
    ```ini
    DB_SERVER=localhost
    DB_PORT=1433
    DB_USER=sa
    DB_PASSWORD=Teste@123
    DB_NAME=master
    DB_DRIVER=ODBC Driver 17 for SQL Server
    ```

4. **Instale as dependências e rode as migrations:**
    ```bash
    uv sync
    uv run alembic upgrade head
    ```

5. **Popule o banco (seed) e inicie a API:**
    ```bash
    uv run python seed.py
    uv run uvicorn app.main:app --reload
    ```

**Acesse a documentação Swagger gerada pelo FastAPI: ```http://localhost:8000/scalar``` (visual moderno) ou ```http://localhost:8000/docs``` (visual padrão FastAPI)**

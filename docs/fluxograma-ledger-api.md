![Fluxograma dos dados (Ledger API)](../app/static/fluxograma-ledger-api.svg "Fluxograma dos dados (Ledger API)")

### Explicando o fluxograma passo a passo

Este diagrama mostra o ciclo de vida de uma requisição `POST /transfer` e como os outros componentes interagem entre si.

#### 1\. Camada de entrada (verde - `api/`)

  * **O porteiro:** O cliente usando swagger envia o JSON. O arquivo `routes.py` recebe.
  * **O fiscal (Pydantic):** Antes de qualquer coisa, o `routes.py` joga os dados para o `Schema`. Se o ID for uma string em vez de inteiro, ou o valor for negativo, o Pydantic barra a entrada e devolve erro 422. O resto do sistema nem fica sabendo que a requisição existiu.

#### 2\. Camada de negócio (azul - `services/`)

  * **O maestro ACID:** Se os dados são válidos, o Route chama o `Service`. É aqui que a transação começa de verdade.
  * O Service não fala SQL. Ele fala "regras de negócio". Ele pede ao repositório: "Me dê as contas X e Y, e tranque-as para que ninguém mais mexa".

#### 3\. Camada de dados (amarelo - `repositories/` & SQLAlchemy)

  * **O tradutor:** O Repository recebe o pedido do Service e traduz para "SQLAlchemy".
  * **O lock crítico:** É aqui que usei o `.with_for_update()`. O SQLAlchemy envia para o SQL Server um comando que diz: *"Leia essas linhas e aplique um bloqueio de escrita (XLOCK) nelas até eu avisar que terminei"*.
  * O Service recebe os objetos de volta, faz a matemática (retira de A, insere em B) na memória do Python.

#### 4\. O banco de dados e a trigger (roxo)

  * **O "momento da verdade" (commit):** O Service devolve "ok" para a rota. A rota diz ao SQLAlchemy: `await db.commit()`.
  * O SQL Server recebe o `COMMIT`. Ele verifica suas **Check Constraints** (saldo \>= 0). Se passar, ele grava os novos saldos no disco permanentemente.
  * **A automação (trigger):** No exato momento em que o SQL Server grava o novo saldo na tabela `accounts`, a **trigger** (que criamos na última etapa) acorda. Ela vê o que mudou, gera o JSON e insere na tabela `audit_logs` silenciosamente. O Python nem sabe que isso aconteceu.

#### 5\. A Resposta

  * Tudo salvo e seguro. A API converte o resultado para JSON (usando o Schema de resposta) e devolve o HTTP 201 para o cliente.

-----

### Conclusão do Projeto

**Stack:**

  * **Linguagem:** Python 3.13 (Async/Await)
  * **Framework Web:** FastAPI
  * **Gerenciador:** uv
  * **Banco de Dados:** SQL Server 2022 (Docker)
  * **ORM & Driver:** SQLAlchemy 2.0 + aioodbc (Async)
  * **Migrações:** Alembic (Async)
  * **Padrão de Arquitetura:** Layered (Service-Repository)
  * **Features Críticas:** Pessimistic Locking, Window Functions, Database Triggers.

# ETL Project: Pipeline de Dados com Arquitetura Medalhão

Projeto de estudo que implementa um pipeline ETL simples em Python, organizado nas camadas **bronze → silver → gold** (arquitetura medalhão). Os dados de usuários são enriquecidos com informações de endereço obtidas na API pública [ViaCEP](https://viacep.com.br) e carregados em um banco PostgreSQL rodando no Docker.

## Arquitetura

```
 users.csv ──► get_data.py ──► cep_info.csv ─┐
 products.json ──────────────────────────────┤
                                             ▼
                              01-bronze-raw (dados brutos)
                                             │  normalize_data.py
                                             ▼
                              02-silver-validated (Parquet limpo)
                                             │  populate_db.py
                                             ▼
                                   PostgreSQL (Docker)
                                             │  03-gold-enriched/query.sql
                                             ▼
                              Dados enriquecidos (usuários + endereço)
```

| Camada | Pasta | Conteúdo |
|---|---|---|
| Bronze | `01-bronze-raw/` | Dados brutos: `users.csv`, `products.json` e `cep_info.csv` (gerado a partir da API ViaCEP) |
| Silver | `02-silver-validated/` | Arquivos Parquet, com listas convertidas em texto e duplicatas removidas |
| Gold | `03-gold-enriched/` | Consulta SQL que une `users` e `cep_info` em uma tabela enriquecida |

## Estrutura do projeto

```
etl-project/
├── 01-bronze-raw/          # dados brutos
├── 02-silver-validated/    # dados validados (Parquet)
├── 03-gold-enriched/       # query.sql com o resultado enriquecido
├── db.py                   # classe DB: conexão, criação de tabelas, inserção e consultas
├── get_data.py             # consulta o ViaCEP para cada CEP dos usuários
├── normalize_data.py       # bronze -> silver
├── populate_db.py          # silver -> PostgreSQL
├── data_view.ipynb         # notebook para explorar os dados
├── docker-compose.yml      # PostgreSQL
├── requirements.txt
└── .env.example            # modelo das variáveis de ambiente
```

## Tecnologias

Python, pandas, PyArrow, Requests, psycopg2, PostgreSQL 18, Docker Compose e Jupyter.

## Como executar

**Pré-requisitos:** Python 3.10+ e Docker.

1. Clone o repositório e crie o ambiente virtual:

   ```bash
   git clone <https://github.com/ASFischer/etl-project.git>
   cd etl-project
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Configure as variáveis de ambiente. Copie o modelo e defina sua própria senha:

   ```bash
   cp .env.example .env            # Windows: copy .env.example .env
   ```

3. Suba o banco de dados:

   ```bash
   docker compose up -d
   ```

4. Execute o pipeline na ordem:

   ```bash
   python get_data.py         # (opcional) consulta o ViaCEP e gera 01-bronze-raw/cep_info.csv
   python normalize_data.py   # bronze -> silver
   python populate_db.py      # silver -> PostgreSQL
   ```

   O `cep_info.csv` já está versionado, então o passo `get_data.py` só é necessário para atualizá-lo.

5. Gere a camada gold executando [`03-gold-enriched/query.sql`](03-gold-enriched/query.sql) no banco (por exemplo, com `docker compose exec db psql -U postgres -d estudo`) ou explore tudo em `data_view.ipynb`.

## Variáveis de ambiente

| Variável | Descrição | Exemplo |
|---|---|---|
| `POSTGRES_HOST` | Host do banco | `localhost` |
| `POSTGRES_PORT` | Porta exposta no host | `1111` |
| `POSTGRES_USER` | Usuário | `postgres` |
| `POSTGRES_PASSWORD` | Senha (defina a sua) | `change_me` |
| `POSTGRES_DB` | Nome do banco | `estudo` |

O arquivo `.env` está no `.gitignore` e nunca deve ser commitado.

## Observações

- `populate_db.py` usa `INSERT` simples: executá-lo mais de uma vez duplica as linhas. Para recomeçar do zero, rode `docker compose down -v` e suba o banco de novo.
- CEPs que o ViaCEP não encontra são ignorados em `get_data.py`.

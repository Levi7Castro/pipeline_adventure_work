# Pipeline AdventureWorks | Data Engineering Project

## 📌 Overview

Pipeline de dados completo utilizando arquitetura **ELT** com **Arquitetura Medallion** (Bronze → Silver → Gold).

O projeto extrai dados do banco **AdventureWorks2022 (SQL Server)**, ingere via **Python + SQLAlchemy + pandas**, carrega em um **Data Warehouse PostgreSQL**, e usa **dbt** para as transformações das camadas Silver e Gold — incluindo modelagem dimensional (fato + dimensões) com testes de qualidade e integridade referencial.

Projeto desenvolvido para demonstrar boas práticas de Engenharia de Dados: ingestão incremental, versionamento de código, modelagem analítica, testes automatizados e documentação técnica honesta (incluindo limitações conhecidas).

---

## 🏗️ Arquitetura

```text
                AdventureWorks2022 (SQL Server)
                            │
                SQLAlchemy + PyODBC (extract)
                            │
                            ▼
                    Pandas DataFrame
                            │
                     to_sql (load)
                            │
                            ▼
              PostgreSQL — Bronze Layer
                            │
                    dbt (staging + dedup)
                            │
                            ▼
                     Silver Layer
                            │
              dbt (modelagem dimensional)
                            │
                            ▼
              Gold Layer (fato + dimensões)
                            │
                            ▼
              Apache Airflow (orquestração)
```

---

## 🚀 Tecnologias

* Python 3.12
* SQLAlchemy + PyODBC (extração SQL Server)
* Pandas (transformação em memória)
* PostgreSQL (Data Warehouse)
* dbt Core (transformações Silver/Gold + testes)
* Apache Airflow (orquestração — em andamento)
* Git / GitHub (versionamento)
* uv (gerenciador de pacotes Python)

---

## 📂 Estrutura do Projeto

```text
dbt_projeto/
├── airflow/
│   ├── dags/
│   └── plugins/
├── ingestion/
│   ├── extract/
│   │   └── extract_generic.py      # extração parametrizada por tabela
│   ├── load/
│   │   └── load_adventure.py       # carga genérica (append/replace)
│   ├── config.py                   # variáveis de ambiente
│   ├── database.py                 # engines SQLAlchemy (SQL Server + Postgres)
│   ├── tables.py                   # config: tabelas, watermark, flags
│   └── main.py                     # orquestra extract → load → watermark
├── pipeline_adventure_work/
│   └── models/
│       ├── silver/                 # staging: dedup + tipagem + rename
│       └── gold/                   # fato + dimensões
├── sql/                            # um .sql por tabela de origem
├── .env                            # credenciais (não versionado)
├── pyproject.toml
└── README.md
```

---

## 📖 Arquitetura Medallion

### 🥉 Bronze
Ingestão bruta das 6 tabelas do AdventureWorks, sem transformação de negócio.

* Extração incremental via watermark (`ModifiedDate`)
* Carga `append` no Postgres (schema `bronze`)
* Metadados de auditoria (`_loaded_at`)
* Watermark persistido em `_meta.ingestion_watermark`

### 🥈 Silver
Staging via dbt: um modelo por tabela de origem.

* Deduplicação por chave primária (`row_number() over (partition by ... order by ModifiedDate desc)`)
* Tipagem correta (ex.: `money` do SQL Server → `numeric(19,4)` no Postgres, evitando perda de precisão)
* Rename para `snake_case`
* Testes `unique` / `not_null` em todas as chaves

### 🥇 Gold
Modelagem dimensional para consumo analítico.

* **`fct_sales`** — fato no grão de linha de pedido (`sales_order_detail_id`)
* **`dim_customer`** — cliente (join `Customer` + `Person`)
* **`dim_product`** — produto
* **`dim_territory`** — território de vendas
* **`dim_date`** — calendário gerado via `generate_series`
* Testes de integridade referencial (`relationships`) entre fato e dimensões

---

## 📊 Tabelas Ingeridas

| Tabela origem | Nome na bronze | Modo de carga |
|---|---|---|
| `Sales.SalesOrderHeader` | `sales_order_header` | Incremental |
| `Sales.SalesOrderDetail` | `sales_order_detail` | Incremental |
| `Production.Product` | `product` | Incremental |
| `Sales.Customer` | `customer` | Full refresh* |
| `Person.Person` | `person` | Full refresh* |
| `Sales.SalesTerritory` | `sales_territory` | Incremental |

---

## ⚙️ Configuração

Crie um arquivo `.env` na raiz do projeto:

```dotenv
SQLSERVER_HOST=
SQLSERVER_PORT=1433
SQLSERVER_DB=AdventureWorks2022
SQLSERVER_USER=
SQLSERVER_PASSWORD=

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=dw
POSTGRES_USER=
POSTGRES_PASSWORD=
```

Pré-requisitos de sistema (Linux/WSL):

```bash
sudo apt install unixodbc unixodbc-dev
# + driver ODBC 18 da Microsoft (ver docs da Microsoft para o repositório)
```

---

## ▶️ Executando

Instalar dependências:

```bash
uv pip install -e .
```

Rodar a ingestão (todas as 6 tabelas, respeitando watermark):

```bash
python -m ingestion.main
```

Forçar recarga completa de todas as tabelas:

```bash
python -m ingestion.main --full-refresh
```

Rodar as transformações dbt:

```bash
cd pipeline_adventure_work
dbt debug
dbt run
dbt test
dbt docs generate
dbt docs serve
```

---


## 📈 Evolução do Projeto

* [x] Estrutura inicial
* [x] Configuração do PostgreSQL
* [x] Configuração do dbt
* [x] Conexão SQL Server
* [x] Extração via SQLAlchemy (genérica, multi-tabela)
* [x] Ingestão incremental com watermark
* [x] Carga Bronze (6 tabelas)
* [x] Modelos Silver (dedup + tipagem + rename, 6 tabelas)
* [x] Modelos Gold (fato + 4 dimensões)
* [x] Testes dbt (unique, not_null, relationships)
* [x] Documentação dbt (`dbt docs generate`)
* [ ] Orquestração com Apache Airflow
* [ ] CI/CD

---

## 🎯 Objetivos Técnicos

* Aplicar Arquitetura Medallion de ponta a ponta
* Implementar pipeline ELT incremental e idempotente
* Utilizar dbt para transformação, tipagem e teste de dados
* Modelar fato e dimensões seguindo boas práticas de BI
* Documentar limitações técnicas de forma transparente
* Automatizar processos com Airflow
* Produzir um projeto completo para portfólio

---

## 👨‍💻 Autor

**Levi Castro**

Projeto desenvolvido para estudos e demonstração de práticas de Engenharia de Dados utilizando Python, SQL Server, PostgreSQL, dbt e Apache Airflow.

LinkedIn: [linkedin.com/in/levi-castro-b231652b7](https://linkedin.com/in/levi-castro-b231652b7)
GitHub: [github.com/Levi7Castro](https://github.com/Levi7Castro)

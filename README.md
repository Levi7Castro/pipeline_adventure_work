# Pipeline AdventureWorks | Data Engineering Project

## 📌 Overview

Este projeto implementa um pipeline de dados completo utilizando uma arquitetura moderna de Engenharia de Dados baseada no conceito **ELT** e na **Arquitetura Medallion**.

A solução extrai dados do banco **AdventureWorks2022 (SQL Server)**, realiza a ingestão utilizando **Python + SQLAlchemy**, persiste os dados em formato **Parquet** e os carrega para um **Data Warehouse PostgreSQL**, onde o **dbt** é responsável pelas transformações das camadas Bronze, Silver e Gold. Todo o fluxo será orquestrado pelo **Apache Airflow**.

O objetivo deste projeto é demonstrar boas práticas de Engenharia de Dados, incluindo organização de código, versionamento, modelagem analítica, qualidade de dados e automação de pipelines.

---

# 🏗️ Arquitetura

```text
                    AdventureWorks2022
                       SQL Server
                            │
                SQLAlchemy + PyODBC
                            │
                            ▼
                    Pandas DataFrame
                            │
                            ▼
                 Parquet (Raw Landing)
                            │
                            ▼
             PostgreSQL - Bronze Layer
                            │
                      dbt Transformations
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
      Bronze            Silver             Gold
                            │
                            ▼
                    Apache Airflow
```

---

# 🚀 Tecnologias

* Python 3.12
* SQLAlchemy
* PyODBC
* Pandas
* PyArrow
* PostgreSQL
* SQL Server
* dbt Core
* Apache Airflow
* Git
* uv (Python Package Manager)

---

# 📂 Estrutura do Projeto

```text
dbt_projeto/

├── airflow/
│   ├── dags/
│   └── plugins/
│
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── docs/
│
├── ingestion/
│   ├── extract/
│   ├── load/
│   ├── transform/
│   ├── config.py
│   ├── database.py
│   └── main.py
│
├── pipeline_adventure_work/
│   ├── models/
│   │   ├── bronze/
│   │   ├── silver/
│   │   └── gold/
│   ├── macros/
│   ├── tests/
│   ├── snapshots/
│   └── dbt_project.yml
│
├── sql/
│
├── .env.example
├── pyproject.toml
└── README.md
```

---

# 📖 Arquitetura Medallion

## 🥉 Bronze

Responsável pela ingestão dos dados exatamente como são recebidos da origem.

Características:

* Dados sem transformação de negócio
* Persistência em Parquet
* Carga para PostgreSQL
* Histórico da origem

---

## 🥈 Silver

Camada responsável pela padronização e preparação dos dados.

Exemplos:

* Conversão de tipos
* Remoção de duplicidades
* Tratamento de valores nulos
* Padronização de colunas
* Aplicação de regras de qualidade

Implementada utilizando **dbt Models**.

---

## 🥇 Gold

Camada analítica.

Responsável pela criação de:

* Fatos
* Dimensões
* Métricas
* Indicadores
* Tabelas para consumo analítico

---

# 🔄 Pipeline

1. Extração do SQL Server
2. Leitura utilizando SQLAlchemy
3. Conversão para DataFrame
4. Persistência em Parquet
5. Carga para PostgreSQL (Bronze)
6. Transformações com dbt
7. Testes de qualidade
8. Publicação das camadas Silver e Gold
9. Orquestração pelo Apache Airflow

---

# 📊 Fonte de Dados

Banco de dados:

* AdventureWorks2022

Tabela inicial utilizada no projeto:

* `Sales.SalesOrderHeader`

O projeto foi estruturado para permitir expansão para múltiplas tabelas.

---

# ⚙️ Configuração

Crie um arquivo `.env` na raiz do projeto.

Exemplo:

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

---

# ▶️ Executando

Criar ambiente virtual:

```bash
uv venv
source .venv/bin/activate
```

Instalar dependências:

```bash
uv sync
```

Executar a ingestão:

```bash
python ingestion/main.py
```

Executar modelos dbt:

```bash
cd pipeline_adventure_work

dbt debug

dbt run

dbt test
```

---

# 📈 Evolução do Projeto

* [x] Estrutura inicial
* [x] Configuração do PostgreSQL
* [x] Configuração do dbt
* [ ] Conexão SQL Server
* [ ] Extração via SQLAlchemy
* [ ] Persistência em Parquet
* [ ] Carga Bronze
* [ ] Modelos Silver
* [ ] Modelos Gold
* [ ] Testes dbt
* [ ] Documentação dbt
* [ ] Orquestração com Apache Airflow
* [ ] CI/CD

---

# 🎯 Objetivos Técnicos

* Aplicar Arquitetura Medallion
* Implementar pipeline ELT
* Utilizar dbt para transformação de dados
* Automatizar processos com Airflow
* Aplicar boas práticas de Engenharia de Dados
* Produzir um projeto completo para portfólio

---

# 👨‍💻 Autor

**Levi Castro**

Projeto desenvolvido para estudos e demonstração de práticas de Engenharia de Dados utilizando Python, PostgreSQL, dbt e Apache Airflow.

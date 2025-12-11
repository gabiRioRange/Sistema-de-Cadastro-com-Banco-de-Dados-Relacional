# 🚀 Sistema de Cadastro Profissional (API RESTful)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![Status](https://img.shields.io/badge/Status-Concluído-success)

## 📋 Sobre o Projeto

Este é um backend robusto desenvolvido em **Python** com **FastAPI**, focado em boas práticas de engenharia de software. O objetivo foi criar um sistema de cadastro escalável, seguro e auditável.

Diferente de CRUDS simples, este projeto implementa **Transacionalidade (ACID)**, **Normalização de Banco de Dados (3FN)** e **Logs de Auditoria via Middleware**, simulando um ambiente real de produção.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Framework Web:** FastAPI (Alta performance e validação automática)
* **ORM:** SQLAlchemy (Abstração de banco de dados relacional)
* **Validação de Dados:** Pydantic & Email-Validator
* **Banco de Dados:** SQLite (Configurado) / PostgreSQL (Pronto para uso)
* **Servidor:** Uvicorn (ASGI)

---

## ✨ Funcionalidades Principais

### 1. CRUD Completo e Robusto
* **Create:** Cadastro de usuários com múltiplos endereços em uma única requisição.
* **Read:** Listagem com **paginação** (skip/limit) e **filtros dinâmicos** (por nome e e-mail).
* **Update:** Atualização de dados cadastrais.
* **Delete:** Remoção segura de registros.

### 2. Segurança e Integridade
* **Transações Atômicas:** Se o cadastro de um endereço falhar, o usuário não é criado (Rollback automático), evitando dados órfãos.
* **Validação Rigorosa:** Schemas Pydantic garantem que nenhum dado inválido chegue ao banco.
* **Auditoria Automática:** Um **Middleware** captura todas as requisições HTTP e salva em uma tabela de `logs_acesso` para auditoria de segurança.

### 3. Arquitetura de Banco de Dados
O banco foi modelado seguindo a **3ª Forma Normal (3FN)**:
* Tabela `usuarios`: Dados cadastrais básicos.
* Tabela `enderecos`: Relacionamento **1:N** (Um usuário pode ter vários endereços).
* Tabela `logs_acesso`: Histórico de operações na API.
* **Índices:** Criados nas colunas de busca frequente (`email`, `nome`) para otimização de performance.

---

## 📂 Estrutura do Projeto

A arquitetura segue o padrão de separação de responsabilidades:

text

    projeto_crud/
    │
    ├── database.py      # Configuração da conexão (Singleton pattern)
    ├── models.py        # Modelos do banco (SQLAlchemy)
    ├── schemas.py       # Serialização e Validação (Pydantic)
    ├── crud.py          # Regras de negócio e Queries otimizadas
    └── main.py          # Rotas da API e Injeção de Dependências

🚀 Como Executar
Pré-requisitos

    Python 3 instalado.

Passo a Passo

Clone o repositório:
Bash

    git clone [https://github.com/gabiRioRange/Sistema-de-Cadastro-com-Banco-de-Dados-Relacional.git](https://github.com/gabiRioRange/Sistema-de-Cadastro-com-Banco-de-Dados-Relacional.git)
    
    cd Sistema-de-Cadastro-com-Banco-de-Dados-Relacional

Instale as dependências:
Bash

    pip install fastapi uvicorn sqlalchemy pydantic email-validator

Execute o servidor:
Bash

    uvicorn main:app --reload

Acesse a Documentação Interativa: O projeto gera documentação automática (Swagger UI). Acesse em seu navegador:

    http://127.0.0.1:8000/docs

🧪 Testando a API
Criar Usuário (POST)

    Endpoint: /usuarios/
    JSON

    {
      "nome": "Gabriel Developer",
      "email": "dev@exemplo.com",
      "enderecos": [
    {
      "rua": "Av. Tecnologia, 100",
      "cidade": "São Paulo",
      "estado": "SP"
    }
      ]
    }

Buscar com Filtros (GET)

    Endpoint: /usuarios/?nome=Gabriel&limit=5
Ver Logs de Auditoria (GET)

    Endpoint: /logs/ (Retorna o histórico de requisições, métodos e datas)
    
👤 Autor
Gabriel Desenvolvedor Python | Ciência da Computação Focado em Backend, IA e Automação.

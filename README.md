# MercadoPro — Fase 1

Sistema web para gerenciamento de mercadinho/supermercado.

## Fase 1
- Estrutura do projeto
- Banco PostgreSQL
- Backend FastAPI
- Autenticação JWT
- Usuários e perfis
- Dashboard inicial
- Tema claro/escuro
- Dados de demonstração

## Requisitos
- Python 3.11+
- Node.js 20+
- PostgreSQL 15+

## Backend
```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

API: http://localhost:8000
Documentação: http://localhost:8000/docs

## Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## Banco
Crie um banco PostgreSQL chamado `mercadopro` e configure o `.env`.

A aplicação cria as tabelas na inicialização para facilitar a primeira execução.
Em produção, utilize migrações Alembic.

## Usuário de demonstração
Usuário: `admin`
Senha: `admin123`

Altere a senha antes de usar o sistema em ambiente real.

## Status
Esta entrega é a Fase 1. Produtos, estoque, compras, PDV, caixa, financeiro, relatórios, backup e integrações fiscais serão desenvolvidos nas próximas fases.

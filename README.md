# MercadoPro — Fase 7

Sistema de gestão para mercadinho com React/Vite + FastAPI + PostgreSQL.

## Fase 7
Financeiro com:
- Contas a pagar
- Contas a receber
- Categorias financeiras
- Lançamentos
- Baixas
- Cancelamentos
- Indicadores financeiros
- Projeção operacional
- Interface premium AI/SaaS em light/dark mode

## Backend
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
Swagger: http://127.0.0.1:8000/docs

## Frontend
```powershell
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## Usuário demo
`admin` / `admin123` — apenas para desenvolvimento.

## Observação
A aplicação cria novas tabelas automaticamente no startup. Para ambientes de produção, use migrações versionadas antes de aplicar alterações de schema.


## Fase 7
Relatórios e Analytics: vendas, produtos, estoque, financeiro, compras e exportação CSV.

## Fase 9 — Integrações
A Fase 9 adiciona o Integration Hub para configuração fiscal e equipamentos. Acesse **Integrações** após entrar como administrador.

### Backend
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

### Frontend
```powershell
cd frontend
npm install
npm run dev
```

Swagger: `http://localhost:8000/docs`

> A emissão fiscal real não é simulada. A configuração de produção depende do certificado, UF, regras tributárias e de um provedor/conector homologado.

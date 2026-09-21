# MercadoPro — Fase 1

Sistema web para gerenciamento de mercadinho/supermercado.

- **Frontend:** React + Vite
- **Backend:** FastAPI + SQLAlchemy + psycopg
- **Banco de dados:** PostgreSQL
- **Autenticação:** JWT

## Funcionalidades da Fase 1
- Estrutura do projeto (backend + frontend)
- Banco PostgreSQL
- Autenticação JWT
- Usuários e perfis
- Dashboard inicial
- Dados de demonstração

---

## Pré-requisitos

Instale, nesta ordem, antes de começar:

| Ferramenta | Versão mínima | Link |
|---|---|---|
| Python | 3.11+ | https://www.python.org/downloads/ |
| Node.js (traz o npm junto) | 20+ | https://nodejs.org/ |
| PostgreSQL | 15+ | https://www.postgresql.org/download/windows/ |
| Git | qualquer recente | https://git-scm.com/download/win |

> ⚠️ **Importante no Windows:** depois de instalar Python, Node.js ou PostgreSQL, **reinicie o computador** (ou pelo menos faça logoff/login) antes de usar os comandos no PowerShell. O Windows só atualiza o PATH (a lista de programas que o terminal reconhece) totalmente após isso. Se um comando como `node`, `npm` ou `psql` "não for reconhecido" logo após instalar, essa é a causa mais comum.

---

## 1. Configurar o banco de dados PostgreSQL

O projeto espera um banco chamado `mercadopro`. Ele **não é criado automaticamente pelo instalador do PostgreSQL** — precisa ser criado manualmente, uma única vez.

### Opção A — usando psql (linha de comando, mais rápido)

O `psql` normalmente não fica no PATH do Windows por padrão. Use o caminho completo (ajuste o número da versão, ex: `18`, `16`, conforme o que você instalou):

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -h localhost -c "CREATE DATABASE mercadopro;"
```

Ele vai pedir a senha do usuário `postgres` (a que você definiu na instalação do PostgreSQL). Se aparecer `CREATE DATABASE`, deu certo.

### Opção B — usando pgAdmin 4 (interface gráfica)

1. Abra o **pgAdmin 4**.
2. No painel esquerdo, expanda **Servers** → seu servidor PostgreSQL (informe a senha se pedido).
3. Clique com o botão direito em **Databases** → **Create** → **Database...**
4. Em **Database**, digite `mercadopro`. Em **Owner**, deixe `postgres`.
5. Clique em **Save**.
6. Confirme que `mercadopro` aparece na lista de bancos.

---

## 2. Configurar e rodar o Backend (FastAPI)

Abra o **PowerShell**, entre na pasta `backend` e execute, um comando por vez:

```powershell
cd caminho\ate\MercadoPro_Fase1\backend

# Criar o ambiente virtual (só na primeira vez)
python -m venv .venv

# Ativar o ambiente virtual (toda vez que for trabalhar no projeto)
.\.venv\Scripts\Activate.ps1

# Instalar as dependências (só na primeira vez, ou quando requirements.txt mudar)
pip install -r requirements.txt

# Copiar o arquivo de variáveis de ambiente de exemplo (só na primeira vez)
copy .env.example .env
```

Depois, **abra o `.env`** (`notepad .env`) e confirme que a linha `DATABASE_URL` tem a senha correta do seu PostgreSQL:

```env
DATABASE_URL=postgresql+psycopg://postgres:SUA_SENHA@localhost:5432/mercadopro
```

Agora suba o servidor:

```powershell
python -m uvicorn app.main:app
```

Resultado esperado:

```text
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

- API: http://127.0.0.1:8000
- Documentação interativa (Swagger): http://127.0.0.1:8000/docs

> ℹ️ Pode aparecer um aviso `(trapped) error reading bcrypt version` no console. É inofensivo — uma incompatibilidade cosmética entre as bibliotecas `passlib` e `bcrypt` que não impede o funcionamento do sistema.

**Deixe este terminal aberto e rodando.** Fechar a janela ou apertar `Ctrl+C` derruba o backend, e o frontend vai parar de conseguir fazer login (erro `Failed to fetch`).

---

## 3. Configurar e rodar o Frontend (React)

Abra um **segundo terminal do PowerShell** (não feche o do backend) e execute:

```powershell
cd caminho\ate\MercadoPro_Fase1\frontend

# Instalar as dependências (só na primeira vez, ou quando package.json mudar)
npm install

# Rodar o servidor de desenvolvimento
npm run dev
```

Resultado esperado:

```text
VITE v6.x.x  ready in ... ms
➜  Local:   http://localhost:5173/
```

Acesse **http://localhost:5173** no navegador.

**Deixe este terminal também aberto e rodando**, junto com o do backend.

---

## 4. Login de demonstração

```text
Usuário: admin
Senha:   admin123
```

⚠️ Altere essa senha antes de usar o sistema em ambiente real.

---

## Resumo do dia a dia (depois que tudo já está instalado)

Sempre que for trabalhar no projeto, você precisa de **dois terminais abertos ao mesmo tempo**:

**Terminal 1 — Backend**
```powershell
cd caminho\ate\MercadoPro_Fase1\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app
```

**Terminal 2 — Frontend**
```powershell
cd caminho\ate\MercadoPro_Fase1\frontend
npm run dev
```

Depois acesse http://localhost:5173.

---

## Solução de problemas comuns

| Erro | Causa provável | Solução |
|---|---|---|
| `psql : termo não reconhecido` | `psql` não está no PATH | Use o caminho completo: `C:\Program Files\PostgreSQL\<versão>\bin\psql.exe` |
| `node`/`npm : termo não reconhecido` | Node.js não instalado, ou PATH não atualizado | Instale o Node.js e **reinicie o computador** |
| `FATAL: autenticação do tipo senha falhou` | Senha do PostgreSQL incorreta no `.env` ou digitada errada | Confira a senha em `backend/.env`, sem espaços extras |
| `FATAL: banco de dados "mercadopro" não existe` | O banco ainda não foi criado | Siga a seção "1. Configurar o banco de dados" acima |
| `Failed to fetch` na tela de login | O backend não está rodando | Verifique se o terminal do backend está aberto e mostrando `Uvicorn running` |
| `ERR_CONNECTION_REFUSED` ao abrir `:8000` ou `:5173` | O respectivo servidor foi fechado/parado | Reinicie o `uvicorn` ou o `npm run dev` naquele terminal |

---

## Estrutura do projeto

```text
MercadoPro_Fase1/
├── backend/
│   ├── .venv/              (ambiente virtual Python — não versionado)
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── requirements.txt
│   ├── .env                (variáveis reais — não versionado)
│   └── .env.example        (modelo de variáveis, versionado)
├── frontend/
│   ├── src/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── docs/
│   └── FASE_1_STATUS.md
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Status

Esta entrega é a **Fase 1**. Produtos, estoque, compras, PDV, caixa, financeiro, relatórios, backup e integrações fiscais serão desenvolvidos nas próximas fases.

# MercadoPro — Fase 10

> **Sistema de gestão para mercadinho | Guia oficial de instalação, configuração e execução**

![MercadoPro](https://img.shields.io/badge/MercadoPro-Fase%2010-2563EB)
![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB)
![Backend](https://img.shields.io/badge/Backend-FastAPI-009688)
![Database](https://img.shields.io/badge/Database-PostgreSQL-336791)

---

## Sumário

1. [Sobre o MercadoPro](#1-sobre-o-mercadopro)
2. [O que existe na Fase 10](#2-o-que-existe-na-fase-10)
3. [Tecnologias utilizadas](#3-tecnologias-utilizadas)
4. [Requisitos](#4-requisitos)
5. [Baixando e extraindo](#5-baixando-e-extraindo)
6. [Estrutura do projeto](#6-estrutura-do-projeto)
7. [Instalando o PostgreSQL](#7-instalando-o-postgresql)
8. [Criando o banco](#8-criando-o-banco)
9. [Configurando o Backend](#9-configurando-o-backend)
10. [Configurando o `.env`](#10-configurando-o-env)
11. [Criando o ambiente Python](#11-criando-o-ambiente-python)
12. [Instalando dependências](#12-instalando-dependências)
13. [Executando a API](#13-executando-a-api)
14. [Configurando o Frontend](#14-configurando-o-frontend)
15. [Instalando dependências do Frontend](#15-instalando-dependências-do-frontend)
16. [Executando o Frontend](#16-executando-o-frontend)
17. [Primeiro acesso](#17-primeiro-acesso)
18. [Verificando o sistema](#18-verificando-o-sistema)
19. [Banco e tabelas](#19-banco-e-tabelas)
20. [Uso em rede local](#20-uso-em-rede-local)
21. [Backup e restauração](#21-backup-e-restauração)
22. [Comandos principais](#22-comandos-principais)
23. [Problemas comuns](#23-problemas-comuns)
24. [Checklist](#24-checklist)
25. [Fases do projeto](#25-fases-do-projeto)
26. [Próximos passos](#26-próximos-passos)

---

# 1. Sobre o MercadoPro

O **MercadoPro** é um sistema de gestão desenvolvido para mercados e pequenos comércios.

A aplicação separa a interface, a API, as regras de negócio, o banco de dados e os módulos administrativos.

A **Fase 10** concentra a profissionalização da interface e da experiência de uso, mantendo os módulos desenvolvidos nas fases anteriores.

O objetivo visual é oferecer aparência de **produto comercial próprio**, com hierarquia, consistência e navegação clara, evitando aparência de template administrativo genérico.

---

# 2. O que existe na Fase 10

## Interface

- Dashboard profissional.
- Sidebar retrátil.
- Navegação organizada por áreas.
- Tema claro.
- Tema escuro.
- Tipografia e espaçamento padronizados.
- Ícones Lucide.
- Tabelas e cards reorganizados.
- Estados de carregamento.
- Estados vazios.
- Feedback visual das ações.
- Layout responsivo.
- Barra superior com busca e usuário.

## Módulos mantidos das fases anteriores

- Dashboard.
- Produtos.
- Categorias.
- Subcategorias.
- Marcas.
- Unidades.
- Estoque.
- Movimentações.
- Fornecedores.
- Compras.
- Clientes.
- PDV.
- Vendas.
- Caixa.
- Financeiro.
- Relatórios.
- Segurança.
- Auditoria.
- Backup.
- Integrações.
- Configurações.

> **Importante:** uma tela de configuração não significa que uma integração externa ou equipamento físico esteja automaticamente operacional. Certificados, drivers, impressoras, balanças, leitores e serviços fiscais exigem configuração específica.

---

# 3. Tecnologias utilizadas

| Camada | Tecnologia | Função |
|---|---|---|
| Frontend | React | Interface |
| Frontend | Vite | Desenvolvimento e build |
| Frontend | JavaScript | Lógica |
| Frontend | CSS | Visual e responsividade |
| Frontend | Lucide | Ícones |
| Backend | Python | Linguagem |
| Backend | FastAPI | API REST |
| Backend | SQLAlchemy | ORM |
| Backend | psycopg | PostgreSQL |
| Backend | JWT | Autenticação |
| Banco | PostgreSQL | Persistência |

---

# 4. Requisitos

## Obrigatórios

- Windows 10 ou Windows 11.
- Python 3.10 ou superior.
- Node.js 20 ou superior.
- npm.
- PostgreSQL.
- PowerShell.

## Recomendados

- 8 GB de RAM ou mais.
- SSD.
- 10 GB de espaço livre.
- Chrome, Edge ou Firefox atualizado.

---

# 5. Baixando e extraindo

Baixe:

```text
MercadoPro_Fase10.zip
```

Extraia, por exemplo, para:

```text
C:\Projetos\MercadoPro_Fase10
```

A estrutura inicial deverá conter pelo menos:

```text
MercadoPro_Fase10
├── backend
├── frontend
├── docs
└── README.md
```

Abra o PowerShell nessa pasta.

Uma forma simples pelo Explorador de Arquivos é abrir a pasta, clicar na barra de endereço, digitar `powershell` e pressionar Enter.

---

# 6. Estrutura do projeto

```text
MercadoPro_Fase10/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── database.py
│   │   ├── main.py
│   │   └── ...
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── package.json
│   └── ...
│
├── docs/
└── README.md
```

### Backend

Responsável pela API, autenticação, banco e regras de negócio.

### Frontend

Responsável pelas telas, navegação, formulários, tabelas, gráficos e experiência do usuário.

---

# 7. Instalando o PostgreSQL

Caso ainda não esteja instalado:

1. Instale o PostgreSQL.
2. Defina uma senha para o usuário `postgres`.
3. Mantenha a porta padrão `5432`.
4. Abra o pgAdmin após a instalação.

Guarde a senha do PostgreSQL. Ela será usada na configuração do backend.

---

# 8. Criando o banco

No pgAdmin:

1. Conecte ao servidor.
2. Clique com o botão direito em **Databases**.
3. Selecione **Create > Database**.
4. Use o nome:

```text
mercadopro
```

5. Salve.

Também é possível usar o terminal:

```powershell
psql -U postgres
```

Depois:

```sql
CREATE DATABASE mercadopro;
```

Para sair:

```sql
\q
```

---

# 9. Configurando o Backend

Entre na pasta:

```powershell
cd backend
```

Confira se existem:

```text
requirements.txt
app\
```

---

# 10. Configurando o `.env`

Dentro de `backend`, crie:

```text
.env
```

Exemplo:

```env
DATABASE_URL=postgresql+psycopg://postgres:SUA_SENHA@localhost:5432/mercadopro
SECRET_KEY=COLOQUE_UMA_CHAVE_LONGA_AQUI
ACCESS_TOKEN_EXPIRE_MINUTES=480
CORS_ORIGINS=http://localhost:5173
```

Substitua `SUA_SENHA` pela senha real do PostgreSQL.

Para gerar uma `SECRET_KEY` aleatória:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Copie o resultado para:

```env
SECRET_KEY=resultado-gerado
```

> **Segurança:** nunca publique o `.env` no GitHub. Ele deve permanecer fora do controle de versão.

---

# 11. Criando o ambiente Python

Dentro de `backend`:

```powershell
python -m venv .venv
```

Ative:

```powershell
.\.venv\Scripts\Activate.ps1
```

O terminal deverá mostrar algo semelhante a:

```text
(.venv) PS C:\Projetos\MercadoPro_Fase10\backend>
```

Se o PowerShell bloquear a ativação:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Depois tente novamente:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

# 12. Instalando dependências

Com `(.venv)` ativo:

```powershell
python -m pip install --upgrade pip
```

Depois:

```powershell
pip install -r requirements.txt
```

Se `pip` não for reconhecido, use:

```powershell
python -m pip install -r requirements.txt
```

---

# 13. Executando a API

Ainda em `backend`:

```powershell
python -m uvicorn app.main:app --reload
```

A API deverá ficar disponível em:

```text
http://localhost:8000
```

A documentação Swagger fica em:

```text
http://localhost:8000/docs
```

**Não feche esse terminal.**

---

# 14. Configurando o Frontend

Abra um **segundo PowerShell** e entre na pasta principal:

```powershell
cd C:\Projetos\MercadoPro_Fase10
```

Depois:

```powershell
cd frontend
```

Confirme que existem:

```text
package.json
src\
```

---

# 15. Instalando dependências do Frontend

Execute:

```powershell
npm install
```

Confira as versões:

```powershell
node --version
npm --version
```

---

# 16. Executando o Frontend

Execute:

```powershell
npm run dev
```

O Vite deverá informar um endereço semelhante a:

```text
http://localhost:5173/
```

Abra esse endereço no navegador.

---

# 17. Primeiro acesso

Abra:

```text
http://localhost:5173
```

No ambiente inicial de demonstração, as credenciais são:

```text
Usuário: admin
Senha: admin123
```

> Altere a senha antes de qualquer utilização real.

---

# 18. Verificando o sistema

O MercadoPro precisa de dois processos ativos.

## Terminal 1 — Backend

```powershell
cd C:\Projetos\MercadoPro_Fase10\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

## Terminal 2 — Frontend

```powershell
cd C:\Projetos\MercadoPro_Fase10\frontend
npm run dev
```

## Endereços

| Serviço | Endereço |
|---|---|
| Frontend | `http://localhost:5173` |
| API | `http://localhost:8000` |
| Swagger | `http://localhost:8000/docs` |

Teste, nesta ordem:

1. Login.
2. Dashboard.
3. Produtos.
4. Estoque.
5. Clientes.
6. Compras.
7. PDV.
8. Caixa.
9. Financeiro.
10. Relatórios.
11. Segurança.
12. Integrações.

---

# 19. Banco e tabelas

O PostgreSQL precisa ter o banco `mercadopro` criado e o usuário configurado no `.env` precisa ter permissão para trabalhar nele.

A aplicação prepara as estruturas necessárias conforme sua implementação atual. Para uma instalação inicial, não é necessário criar manualmente cada tabela pelo pgAdmin.

Antes de uma atualização importante, faça backup do banco.

---

# 20. Uso em rede local

Depois que o sistema funcionar no próprio computador, ele pode ser preparado para outros computadores da rede.

Exemplo:

```text
Servidor: 10.0.0.10
Backend: 10.0.0.10:8000
Frontend: 10.0.0.10:5173
```

Para isso, também será necessário configurar:

- Firewall do Windows.
- CORS.
- Endereço de escuta do backend.
- Acesso ao PostgreSQL.
- Regras da rede local.
- Segurança de acesso.

Durante a instalação inicial, mantenha `localhost`.

---

# 21. Backup e restauração

## Backup em formato customizado

```powershell
pg_dump -U postgres -h localhost -p 5432 -F c -b -v -f mercadopro_backup.dump mercadopro
```

## Backup SQL

```powershell
pg_dump -U postgres -h localhost -p 5432 -F p -f mercadopro_backup.sql mercadopro
```

## Restauração

Exemplo para um banco preparado para receber a restauração:

```powershell
pg_restore -U postgres -h localhost -p 5432 -d mercadopro -v mercadopro_backup.dump
```

Antes de restaurar, confirme o banco de destino, faça um backup recente e garanta que nenhum usuário esteja trabalhando durante a operação.

---

# 22. Comandos principais

## Backend

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Sair do ambiente virtual:

```powershell
deactivate
```

## Frontend

```powershell
cd frontend
npm install
npm run dev
```

Build de produção:

```powershell
npm run build
```

Pré-visualização do build:

```powershell
npm run preview
```

---

# 23. Problemas comuns

## Python não é reconhecido

```powershell
python --version
```

Se falhar, instale o Python e habilite a opção **Add Python to PATH**.

## Uvicorn não é reconhecido

Use:

```powershell
python -m uvicorn app.main:app --reload
```

Confirme que `(.venv)` aparece no terminal.

## Erro de conexão com PostgreSQL

Confira:

- PostgreSQL está ligado.
- Porta `5432` está correta.
- Banco é `mercadopro`.
- Usuário está correto.
- Senha está correta.
- `DATABASE_URL` está correta.

Exemplo:

```env
DATABASE_URL=postgresql+psycopg://postgres:SENHA@localhost:5432/mercadopro
```

## `npm` não é reconhecido

```powershell
node --version
npm --version
```

Se falhar, instale o Node.js e abra um novo PowerShell.

## `vite is not recognized`

Dentro de `frontend`:

```powershell
npm install
npm run dev
```

## Porta 8000 ocupada

```powershell
netstat -ano | findstr :8000
```

## Porta 5173 ocupada

```powershell
netstat -ano | findstr :5173
```

Se o navegador abrir, mas os dados não aparecerem, confira o backend em `http://localhost:8000/docs` e use `F12 > Console` e `F12 > Network` no navegador.

---

# 24. Checklist

## Ambiente

- [ ] Windows instalado.
- [ ] Python instalado.
- [ ] Node.js instalado.
- [ ] npm funcionando.
- [ ] PostgreSQL instalado.
- [ ] pgAdmin funcionando.

## Banco

- [ ] PostgreSQL iniciado.
- [ ] Banco `mercadopro` criado.
- [ ] Usuário configurado.
- [ ] Senha conferida.
- [ ] Porta `5432` disponível.

## Backend

- [ ] `.venv` criado.
- [ ] `.venv` ativado.
- [ ] Dependências instaladas.
- [ ] `.env` criado.
- [ ] `DATABASE_URL` configurada.
- [ ] `SECRET_KEY` configurada.
- [ ] API iniciada.
- [ ] `/docs` funcionando.

## Frontend

- [ ] `npm install` executado.
- [ ] `npm run dev` executado.
- [ ] `localhost:5173` abrindo.
- [ ] Login funcionando.

## Testes funcionais

- [ ] Dashboard.
- [ ] Produtos.
- [ ] Estoque.
- [ ] Compras.
- [ ] Clientes.
- [ ] PDV.
- [ ] Caixa.
- [ ] Financeiro.
- [ ] Relatórios.
- [ ] Segurança.
- [ ] Integrações.

---

# 25. Fases do projeto

| Fase | Objetivo |
|---|---|
| Fase 1 | Estrutura, banco, autenticação e usuários |
| Fase 2 | Produtos, categorias, marcas e estoque |
| Fase 3 | Fornecedores e compras |
| Fase 4 | Clientes, PDV e vendas |
| Fase 5 | Caixa e pagamentos |
| Fase 6 | Financeiro |
| Fase 7 | Relatórios |
| Fase 8 | Segurança, auditoria e backup |
| Fase 9 | Integrações e equipamentos |
| Fase 10 | Profissionalização da interface e UX |

A Fase 10 utiliza a base construída nas fases anteriores e não deve ser instalada como um projeto isolado de uma versão anterior.

---

# 26. Próximos passos

Antes de colocar o MercadoPro em produção, recomenda-se uma etapa específica de estabilização:

1. Testes automatizados.
2. Aplicação completa das permissões por rota.
3. Migrações controladas do banco.
4. Backup automático.
5. Teste real de restauração.
6. Controle de sessões.
7. Segurança de produção.
8. HTTPS.
9. Integração fiscal real.
10. Impressoras.
11. Leitores de código de barras.
12. Balanças.
13. Testes completos do PDV.
14. Testes de fechamento de caixa.
15. Testes de concorrência.
16. Testes de recuperação após falhas.

---

# Inicialização rápida

Depois da instalação inicial, são necessários dois terminais.

## Terminal 1

```powershell
cd C:\Projetos\MercadoPro_Fase10\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

## Terminal 2

```powershell
cd C:\Projetos\MercadoPro_Fase10\frontend
npm run dev
```

Depois abra:

```text
http://localhost:5173
```

---

# Segurança

Nunca publique no GitHub:

- `.env`;
- senha do PostgreSQL;
- `SECRET_KEY`;
- certificados digitais;
- tokens;
- credenciais de serviços;
- backups do banco;
- dados reais de clientes.

Use dados de teste durante o desenvolvimento.

Antes de produção, altere as credenciais de demonstração e faça um backup inicial do banco.

---

## MercadoPro

**Sistema de gestão para seu mercado.**

**Fase 10 — Interface, experiência e preparação para evolução do produto.**

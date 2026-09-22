MercadoPro — Fase 10

Guia completo de instalação, configuração e execução

Este documento explica, desde o início, como baixar, preparar e executar o MercadoPro — Fase 10 em um computador Windows.

A versão possui:

Frontend em React + Vite

Backend em Python + FastAPI

Banco PostgreSQL

SQLAlchemy + psycopg

Autenticação com JWT

Dashboard e módulos das fases anteriores

Interface profissional da Fase 10

Tema claro e escuro

Sidebar retrátil

Ícones Lucide

Relatórios

Financeiro

PDV

Estoque

Compras

Segurança

Integrações

Scripts de backup e restauração do PostgreSQL

1. O que você precisa instalar

Antes de abrir o sistema, recomendamos instalar os seguintes programas.

1.1 Python

Baixe uma versão atual do Python 3.x para Windows.

Durante a instalação, marque:

Add Python to PATH

Depois abra o PowerShell e teste:

python --version

Exemplo esperado:

Python 3.12.x

Se python não funcionar, teste:

py --version

2. Instalar Node.js

O frontend React precisa do Node.js e do npm.

Depois de instalar, abra um novo PowerShell e execute:

node --version
npm --version

Você deverá receber duas versões.

Exemplo:

v22.x.x
10.x.x

Não é necessário instalar React separadamente. O npm install fará isso pelo projeto.

3. Instalar PostgreSQL

O MercadoPro utiliza PostgreSQL.

Durante a instalação do PostgreSQL, anote:

usuário: normalmente postgres

senha definida na instalação

porta: normalmente 5432

Também é recomendável instalar o pgAdmin, que facilita a administração do banco.

Depois confirme se o PostgreSQL está funcionando.

No Windows, procure por:

Serviços

E confirme que o serviço do PostgreSQL está iniciado.

4. Baixar o projeto

Baixe o arquivo:

MercadoPro_Fase10.zip

Depois extraia para uma pasta simples.

Exemplo:

C:\MercadoPro\MercadoPro_Fase10

Evite inicialmente colocar o projeto em uma pasta muito profunda.

Depois de extrair, a estrutura deve ficar parecida com:

MercadoPro_Fase10
│
├── backend
│   ├── app
│   ├── requirements.txt
│   └── .env.example
│
├── frontend
│   ├── src
│   ├── package.json
│   └── ...
│
├── scripts
│   └── backups
│
├── docs
│
├── docker-compose.yml
└── .gitignore

5. Criar o banco de dados

Você pode fazer isso de duas formas.

Opção A — PostgreSQL instalado no Windows

Abra o pgAdmin.

Crie um banco chamado:

mercadopro

O nome precisa ser exatamente esse se você utilizar o .env.example como base.

Configuração típica:

Host: localhost
Porta: 5432
Banco: mercadopro
Usuário: postgres
Senha: a senha que você definiu no PostgreSQL

Não precisa criar as tabelas manualmente. O backend cria a estrutura inicial quando inicia.

6. Opção B — PostgreSQL usando Docker

Se você já usa Docker Desktop, o projeto possui um docker-compose.yml.

Abra o PowerShell dentro da pasta do projeto:

cd C:\MercadoPro\MercadoPro_Fase10

Execute:

docker compose up -d

Verifique:

docker ps

Deve aparecer o container:

mercadopro-postgres

Nesta configuração o banco utiliza:

Banco: mercadopro
Usuário: postgres
Senha: postgres
Porta: 5432

Importante: escolha uma estratégia. Se você já possui PostgreSQL local usando a porta 5432, não inicie o PostgreSQL do Docker na mesma porta sem ajustar a configuração.

7. Configurar o Backend

Entre na pasta backend:

cd C:\MercadoPro\MercadoPro_Fase10\backend

Crie o ambiente virtual:

python -m venv .venv

Ative:

.\.venv\Scripts\Activate.ps1

Se o PowerShell bloquear a ativação, execute uma vez:

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

Depois:

.\.venv\Scripts\Activate.ps1

Você deverá ver algo parecido com:

(.venv) PS C:\MercadoPro\MercadoPro_Fase10\backend>

8. Instalar as dependências Python

Com o ambiente virtual ativado:

python -m pip install --upgrade pip

Depois:

pip install -r requirements.txt

Aguarde a instalação terminar.

Se aparecer erro de compilação ou pacote, copie o erro completo antes de tentar alterar o projeto.

9. Criar o arquivo .env

Dentro de:

MercadoPro_Fase10\backend

existe:

.env.example

Faça uma cópia chamada:

.env

O arquivo deve ficar:

backend\.env

Não deixe como:

.env.txt

No Windows Explorer, habilite a opção de mostrar extensões se necessário.

10. Configurar o .env

O modelo possui esta estrutura:

DATABASE_URL=postgresql+psycopg://postgres:SUA_SENHA@localhost:5432/mercadopro
SECRET_KEY=GERE_UMA_CHAVE_LONGA_E_ALEATORIA
ACCESS_TOKEN_EXPIRE_MINUTES=480
CORS_ORIGINS=http://localhost:5173

Troque SUA_SENHA pela senha real do PostgreSQL.

Exemplo:

DATABASE_URL=postgresql+psycopg://postgres:MINHA_SENHA@localhost:5432/mercadopro
SECRET_KEY=uma-chave-grande-e-aleatoria
ACCESS_TOKEN_EXPIRE_MINUTES=480
CORS_ORIGINS=http://localhost:5173

Se a senha possuir caracteres especiais, como @, :, /, # ou %, ela pode precisar ser codificada na URL do banco. Se isso acontecer, envie o erro apresentado pelo sistema antes de alterar outras configurações.

Nunca publique o .env real no GitHub.

11. Gerar uma SECRET_KEY melhor

Para gerar uma chave aleatória usando o Python:

python -c "import secrets; print(secrets.token_urlsafe(64))"

Copie o resultado para:

SECRET_KEY=COLE_AQUI_A_CHAVE

12. Testar o banco antes de iniciar

Confirme primeiro:

PostgreSQL está ligado

banco mercadopro existe

usuário está correto

senha está correta

porta está correta

.env está dentro de backend

Se o PostgreSQL estiver local:

localhost:5432

13. Iniciar o Backend

Ainda dentro de:

backend

com (.venv) aparecendo no PowerShell:

python -m uvicorn app.main:app --reload

Se tudo estiver correto, deverá aparecer algo semelhante a:

Uvicorn running on http://127.0.0.1:8000

Não feche essa janela enquanto estiver usando o sistema.

14. Testar a API

Abra o navegador:

http://localhost:8000/docs

Essa é a documentação interativa do FastAPI.

Se aparecer a página do Swagger, o backend está funcionando.

15. Configurar o Frontend

Abra um segundo PowerShell.

Entre na pasta frontend:

cd C:\MercadoPro\MercadoPro_Fase10\frontend

Instale as dependências:

npm install

A primeira instalação pode demorar alguns minutos.

16. Iniciar o Frontend

Depois do npm install:

npm run dev

O Vite deverá informar um endereço parecido com:

http://localhost:5173/

Abra no navegador:

http://localhost:5173

17. Ordem correta para abrir o sistema

Sempre que for trabalhar localmente:

Janela 1 — Banco

Se usar PostgreSQL local, confirme que o serviço está ligado.

Se usar Docker:

docker compose up -d

Janela 2 — Backend

cd C:\MercadoPro\MercadoPro_Fase10\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload

Janela 3 — Frontend

cd C:\MercadoPro\MercadoPro_Fase10\frontend
npm run dev

Depois abra:

http://localhost:5173

18. Primeiro acesso

O projeto possui usuário administrativo de demonstração criado pelo backend.

Credenciais de desenvolvimento:

Usuário: admin
Senha: admin123

Essas credenciais são apenas para desenvolvimento/demonstração.

Em um ambiente real, altere a senha e não mantenha credenciais padrão.

19. Como saber se está tudo funcionando

Faça este checklist:

[ ] PostgreSQL iniciado
[ ] Banco mercadopro criado
[ ] backend/.env criado
[ ] DATABASE_URL configurada
[ ] SECRET_KEY configurada
[ ] Ambiente virtual Python ativado
[ ] requirements.txt instalado
[ ] Backend iniciado
[ ] http://localhost:8000/docs abre
[ ] npm install concluído
[ ] Frontend iniciado
[ ] http://localhost:5173 abre
[ ] Login funcionando
[ ] Dashboard abre

20. Estrutura das principais pastas

backend

Contém a API e as regras de negócio.

backend/app/
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py
│
├── models/
│   └── models.py
│
├── routers/
│   ├── auth.py
│   ├── dashboard.py
│   ├── products.py
│   ├── inventory.py
│   ├── purchases.py
│   ├── sales.py
│   ├── cash.py
│   ├── finance.py
│   ├── reports.py
│   ├── security.py
│   └── integrations.py
│
└── main.py

frontend

Contém a interface React.

frontend/
├── src/
│   ├── App.jsx
│   ├── styles.css
│   └── services/
│       └── api.js
│
├── package.json
└── ...

21. Backup do PostgreSQL

Na pasta:

scripts\backups

existem:

backup_postgres.ps1
restore_postgres.ps1

O backup utiliza pg_dump.

Para isso, o PostgreSQL precisa ter as ferramentas de linha de comando disponíveis no PATH ou ser executado com o caminho correto do PostgreSQL.

Antes de utilizar em produção, faça um teste de backup e restauração em uma base de teste.

22. Executar backup

Abra PowerShell na pasta do projeto:

cd C:\MercadoPro\MercadoPro_Fase10

Execute o script:

.\scripts\backups\backup_postgres.ps1

O objetivo é gerar um arquivo de backup do banco.

Não considere o backup válido apenas porque o script terminou sem mensagem de erro. Sempre confira se o arquivo foi criado e faça testes periódicos de restauração.

23. Restauração do banco

O arquivo:

scripts\backups\restore_postgres.ps1

é destinado à restauração.

ATENÇÃO:

A restauração pode substituir dados existentes.

Nunca teste restauração diretamente no banco de produção sem confirmar o procedimento.

Recomendação:

Criar um banco de teste.

Restaurar o backup nele.

Conferir produtos.

Conferir clientes.

Conferir vendas.

Conferir estoque.

Conferir financeiro.

Somente depois estabelecer o procedimento oficial.

24. Problema: python não é reconhecido

Teste:

py --version

Se funcionar, crie o ambiente com:

py -m venv .venv

Se nenhum comando funcionar, o Python provavelmente não foi adicionado ao PATH.

25. Problema: PowerShell bloqueia .venv

Erro típico:

running scripts is disabled on this system

Execute:

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

Depois:

.\.venv\Scripts\Activate.ps1

26. Problema: ModuleNotFoundError

Primeiro confirme que o ambiente virtual está ativo:

(.venv)

Depois:

pip install -r requirements.txt

Não instale pacotes aleatórios antes de verificar o erro completo.

27. Problema: banco não conecta

Confira o .env:

DATABASE_URL=postgresql+psycopg://postgres:SUA_SENHA@localhost:5432/mercadopro

Verifique:

PostgreSQL ligado.

Banco mercadopro existente.

Usuário correto.

Senha correta.

Porta 5432 livre/correta.

Não existem dois PostgreSQL disputando a mesma porta.

28. Problema: database mercadopro does not exist

Crie o banco no pgAdmin:

Databases
  └── Create
      └── Database
          └── mercadopro

Depois reinicie o backend.

29. Problema: frontend não abre

Confira se o frontend está rodando:

npm run dev

Se aparecer:

vite: not found

execute:

npm install

Depois:

npm run dev

30. Problema: npm install demora muito

Primeiro aguarde alguns minutos.

Se realmente travar, feche somente o processo do npm e tente novamente.

Confira:

node --version
npm --version

Não apague o projeto inteiro por causa de uma instalação incompleta.

31. Problema: porta 8000 ocupada

O backend utiliza normalmente:

8000

Você pode verificar no Windows:

netstat -ano | findstr :8000

Se outro processo estiver utilizando a porta, encerre o processo somente se tiver certeza de que ele pode ser fechado.

32. Problema: porta 5173 ocupada

Verifique:

netstat -ano | findstr :5173

O Vite pode escolher outra porta automaticamente, dependendo da configuração.

Sempre utilize o endereço mostrado no terminal.

33. Como parar o sistema

No terminal do backend:

Ctrl + C

No terminal do frontend:

Ctrl + C

Se estiver usando Docker:

docker compose down

34. O que NÃO fazer

Não apague:

backend/app
frontend/src

Não altere o banco manualmente sem necessidade.

Não publique:

backend/.env

Não coloque senha real no GitHub.

Não execute scripts de restauração em produção sem conferir o banco de destino.

Não reinstale PostgreSQL só porque apareceu um erro de conexão. Primeiro verifique serviço, banco, porta e .env.

35. Fluxo recomendado para desenvolvimento

Quando for desenvolver uma nova funcionalidade:

Inicie PostgreSQL.

Inicie o backend.

Confirme /docs.

Inicie o frontend.

Abra o MercadoPro.

Teste a funcionalidade.

Confira o banco.

Confira os logs do backend.

Só depois faça alterações maiores.

36. Endereços principais

Aplicação:

http://localhost:5173

API:

http://localhost:8000

Swagger:

http://localhost:8000/docs

Documentação alternativa da API:

http://localhost:8000/redoc

37. Arquivos importantes

backend/.env

Configuração do banco e segurança.

backend/requirements.txt

Dependências Python.

frontend/package.json

Dependências e comandos do frontend.

docker-compose.yml

Configuração opcional do PostgreSQL via Docker.

scripts/backups/

Scripts de backup e restauração.

docs/

Status e documentação das fases.

38. Fase 10 — o que mudou visualmente

A Fase 10 concentra a evolução de UI/UX.

Principais pontos:

nova hierarquia visual;

sidebar profissional;

sidebar retrátil;

ícones consistentes;

ausência de emojis como elementos principais da interface;

dashboard reorganizado;

cards com menos excesso visual;

melhor contraste;

dark mode refinado;

light mode refinado;

responsividade;

transições discretas;

melhor organização dos módulos.

As funcionalidades de negócio das fases anteriores continuam fazendo parte da aplicação.

39. Observação importante sobre produção

Esta versão é adequada para continuar o desenvolvimento e os testes locais.

Antes de colocar o MercadoPro em uma operação comercial real, ainda é necessário realizar uma etapa específica de preparação para produção, incluindo:

servidor de produção;

HTTPS;

domínio;

banco com política de backup;

restauração testada;

política de usuários e permissões;

monitoramento;

logs;

segurança de credenciais;

configuração fiscal conforme a operação real;

testes com equipamentos reais;

testes de concorrência;

testes de fechamento de caixa;

testes de venda e estorno;

testes de estoque;

testes financeiros.

Não trate a existência de uma tela como prova de que uma integração fiscal ou equipamento físico está pronto para produção.

40. Checklist final de instalação

Use esta sequência exatamente na primeira instalação:

1. Instalar Python
2. Instalar Node.js
3. Instalar PostgreSQL ou preparar Docker
4. Extrair MercadoPro_Fase10.zip
5. Criar banco mercadopro
6. Entrar em backend
7. Criar .venv
8. Ativar .venv
9. Instalar requirements.txt
10. Copiar .env.example para .env
11. Configurar DATABASE_URL
12. Configurar SECRET_KEY
13. Iniciar backend
14. Abrir http://localhost:8000/docs
15. Abrir outro PowerShell
16. Entrar em frontend
17. Executar npm install
18. Executar npm run dev
19. Abrir http://localhost:5173
20. Fazer login
21. Testar dashboard
22. Testar produtos
23. Testar estoque
24. Testar PDV
25. Testar compras
26. Testar financeiro
27. Testar relatórios
28. Testar segurança
29. Testar integrações
30. Fazer um backup de teste

41. Comandos resumidos

Backend

cd C:\MercadoPro\MercadoPro_Fase10\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

Frontend

Em outro PowerShell:

cd C:\MercadoPro\MercadoPro_Fase10\frontend
npm install
npm run dev

Docker PostgreSQL

Na raiz do projeto:

docker compose up -d

Para parar:

docker compose down

42. Regra principal

Se alguma coisa der errado, não reinstale tudo imediatamente.

Primeiro identifique em qual camada está o problema:

Banco
  ↓
Backend / API
  ↓
Frontend
  ↓
Navegador

Por exemplo:

/docs não abre → investigar backend.

/docs abre, mas login falha → investigar API/banco/autenticação.

API funciona, mas página não abre → investigar frontend.

Tela abre, mas dados não aparecem → investigar API, banco e console do navegador.

Essa separação evita perder configurações que já estão funcionando.

MercadoPro

Fase atual: 10 — Professional UI / UX

Base tecnológica:

React
Vite
FastAPI
Python
PostgreSQL
SQLAlchemy
JWT
Lucide React

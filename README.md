

readme = r"""# MercadoPro — Fase 10

> **Sistema de gestão para mercadinho | Guia oficial de instalação, configuração e execução**

![MercadoPro](https://img.shields.io/badge/MercadoPro-Fase%2010-2563EB)
![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB)
![Backend](https://img.shields.io/badge/Backend-FastAPI-009688)
![Database](https://img.shields.io/badge/Database-PostgreSQL-336791)
![Python](https://img.shields.io/badge/Python-3.12-3776AB)
![Node](https://img.shields.io/badge/Node.js-20%2B-339933)

---

## Sumário

1. [Sobre o MercadoPro](#1-sobre-o-mercadopro)
2. [O que existe na Fase 10](#2-o-que-existe-na-fase-10)
3. [Tecnologias utilizadas](#3-tecnologias-utilizadas)
4. [Requisitos do computador](#4-requisitos-do-computador)
5. [Baixando e extraindo o projeto](#5-baixando-e-extraindo-o-projeto)
6. [Estrutura do projeto](#6-estrutura-do-projeto)
7. [Instalando o PostgreSQL](#7-instalando-o-postgresql)
8. [Criando o banco de dados](#8-criando-o-banco-de-dados)
9. [Configurando o Backend](#9-configurando-o-backend)
10. [Configurando o arquivo `.env`](#10-configurando-o-arquivo-env)
11. [Criando o ambiente virtual Python](#11-criando-o-ambiente-virtual-python)
12. [Instalando as dependências do Backend](#12-instalando-as-dependências-do-backend)
13. [Executando a API](#13-executando-a-api)
14. [Configurando o Frontend](#14-configurando-o-frontend)
15. [Instalando as dependências do Frontend](#15-instalando-as-dependências-do-frontend)
16. [Executando o Frontend](#16-executando-o-frontend)
17. [Primeiro acesso](#17-primeiro-acesso)
18. [Como verificar se tudo está funcionando](#18-como-verificar-se-tudo-está-funcionando)
19. [Banco de dados e criação das tabelas](#19-banco-de-dados-e-criação-das-tabelas)
20. [Configuração para uso em rede local](#20-configuração-para-uso-em-rede-local)
21. [Backup e restauração](#21-backup-e-restauração)
22. [Comandos mais utilizados](#22-comandos-mais-utilizados)
23. [Problemas comuns](#23-problemas-comuns)
24. [Checklist de instalação](#24-checklist-de-instalação)
25. [Estrutura das fases do MercadoPro](#25-estrutura-das-fases-do-mercadopro)
26. [Próximos passos](#26-próximos-passos)

---

# 1. Sobre o MercadoPro

O **MercadoPro** é um sistema de gestão desenvolvido para operações de mercado, mercadinho e comércio de produtos.

A aplicação foi construída para separar claramente:

- interface do usuário;
- API;
- regras de negócio;
- banco de dados;
- autenticação;
- auditoria;
- módulos administrativos;
- integrações.

A **Fase 10** concentra principalmente a evolução visual e de experiência do sistema, mantendo os módulos construídos nas fases anteriores.

O objetivo é que o MercadoPro tenha aparência de um **produto comercial profissional**, evitando a aparência de um painel administrativo genérico.

---

# 2. O que existe na Fase 10

A Fase 10 trabalha principalmente a camada de **UI/UX**, sem abandonar as funcionalidades reais construídas anteriormente.

## Interface

- Dashboard profissional.
- Sidebar retrátil.
- Navegação organizada por áreas.
- Tema claro.
- Tema escuro.
- Tipografia padronizada.
- Espaçamento consistente.
- Ícones Lucide.
- Cards com hierarquia visual.
- Tabelas mais organizadas.
- Estados de carregamento.
- Estados vazios.
- Feedback visual das ações.
- Layout responsivo.
- Barra superior com busca e informações do usuário.
- Visual mais limpo e menos dependente de gradientes.

## Módulos existentes

O projeto mantém os principais módulos desenvolvidos nas fases anteriores:

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

> **Importante:** a existência de uma tela de configuração não significa que toda integração física ou fiscal esteja automaticamente operacional. Equipamentos, certificados digitais e serviços externos dependem de configuração específica.

---

# 3. Tecnologias utilizadas

## Frontend

| Tecnologia | Função |
|---|---|
| React | Construção da interface |
| Vite | Servidor de desenvolvimento e build |
| JavaScript | Lógica da aplicação |
| CSS | Identidade visual e responsividade |
| Lucide | Ícones da interface |

## Backend

| Tecnologia | Função |
|---|---|
| Python | Linguagem do backend |
| FastAPI | API REST |
| SQLAlchemy | ORM |
| psycopg | Comunicação com PostgreSQL |
| JWT | Autenticação |

## Banco de dados

| Tecnologia | Função |
|---|---|
| PostgreSQL | Banco principal |

---

# 4. Requisitos do computador

Para executar o projeto localmente no Windows, recomendamos:

### Obrigatório

- Windows 10 ou Windows 11.
- Python 3.10 ou superior.
- Node.js 20 ou superior.
- npm.
- PostgreSQL.
- PowerShell.
- Git, caso o projeto seja baixado por repositório.

### Recomendado

- 8 GB de RAM ou mais.
- SSD.
- 10 GB de espaço livre.
- Navegador atualizado:
  - Google Chrome;
  - Microsoft Edge;
  - Firefox.

---

# 5. Baixando e extraindo o projeto

Depois de baixar o arquivo:

```text
MercadoPro_Fase10.zip

# MercadoPro — Status da Fase 1

## ✅ Concluído
- Estrutura separada de frontend e backend.
- PostgreSQL configurado via variável de ambiente.
- FastAPI com documentação automática.
- Modelo inicial de usuários.
- Modelo inicial de permissões.
- Configurações do sistema.
- Auditoria inicial.
- Autenticação com JWT.
- Login funcional.
- Proteção de rota `/api/auth/me`.
- Dashboard funcional consumindo API.
- Tema claro/escuro.
- Layout responsivo.
- Usuário administrador de demonstração.

## 🟡 Parcial
- Permissões existem no banco, mas a tela de administração de permissões ainda será implementada.
- Auditoria possui estrutura, mas os eventos completos serão ligados aos módulos nas próximas fases.
- Dashboard possui os cartões e endpoints, mas os números reais dependem dos módulos de vendas, estoque e financeiro.

## ❌ Ainda falta
- CRUD de usuários.
- Tela de permissões.
- Produtos.
- Categorias.
- Estoque.
- PDV.
- Caixa.
- Financeiro.
- Relatórios.
- Backup.
- Integrações fiscais e equipamentos.

## 🐛 Problemas conhecidos
- Nenhum erro conhecido no código-base desta entrega; a execução depende de PostgreSQL, Python e Node instalados corretamente.
- O banco inicial é criado automaticamente para facilitar o desenvolvimento. Para produção, migrar para Alembic.

## 🔧 Correções/decisões
- Senhas não são armazenadas em texto puro.
- Token JWT é usado para sessão.
- CORS fica configurável por `.env`.
- Dados do dashboard são explicitamente marcados como demonstração até os módulos de negócio existirem.

## ➡️ Próxima etapa
FASE 2 — Produtos, categorias, marcas e estoque.

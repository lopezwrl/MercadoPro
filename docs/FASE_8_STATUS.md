# MercadoPro — Fase 8 · Auditoria, Backup e Segurança

## Objetivo
Adicionar uma camada operacional de segurança sem quebrar as fases anteriores: gestão de usuários, perfis, matriz de permissões, auditoria, troca de senha, headers HTTP e scripts de backup/restauração PostgreSQL.

## Implementado de verdade
- Backend FastAPI `/api/security`.
- Gestão de usuários por administrador: criar, editar perfil/status e consultar.
- Perfis: ADMINISTRADOR, GERENTE, CAIXA, ESTOQUE e FINANCEIRO.
- Matriz de permissões por módulo com visualizar/criar/editar/excluir.
- Consulta de auditoria com filtro por período, ação, usuário e texto.
- Alteração da própria senha.
- Proteção das rotas do Security Center para ADMINISTRADOR.
- Headers HTTP de segurança e `Cache-Control: no-store` nas rotas `/api`.
- Scripts PowerShell de backup e restauração PostgreSQL em `scripts/backups/`.
- `.env.example` para separar configuração e segredo do código.
- Nova página visual `Segurança` integrada ao mesmo padrão SaaS/IA das fases 5–7.

## Auditoria
As fases anteriores já registravam várias ações em `auditoria` (produtos, estoque, vendas, compras, fornecedores e financeiro). A Fase 8 cria a central para consultar esses eventos.

## Backup
O backup é feito pelo `pg_dump` diretamente, e não pela API. Isso evita expor credenciais e arquivos de banco pela aplicação web.

### Backup
```powershell
.\scripts\backups\backup_postgres.ps1
```

### Restauração
```powershell
.\scripts\backups\restore_postgres.ps1 -BackupFile .\backups\mercadopro_YYYYMMDD_HHMMSS.dump
```

A restauração exige digitar `RESTAURAR` e deve ser tratada como operação administrativa.

## Segurança importante
- O usuário demo `admin/admin123` continua presente para desenvolvimento. Antes de produção, altere a senha.
- Em produção, `SECRET_KEY` deve ser longa e aleatória.
- O arquivo `backend/.env` não deve ser enviado ao Git.
- Os scripts de backup devem ser executados em ambiente com acesso ao PostgreSQL e `pg_dump/pg_restore` no PATH.

## Parcial / próximo endurecimento
- A matriz de permissões está armazenada e administrável, mas as regras de autorização ainda não foram aplicadas automaticamente a todas as operações de cada módulo.
- O JWT continua stateless; ainda não há revogação individual de token/sessão no banco.
- Não há 2FA.
- Não há agendamento automático de backup pelo sistema.
- O frontend build não foi validado neste ambiente porque as dependências npm/Vite não estavam disponíveis; backend passou por `compileall`.

## Arquivos principais
- `backend/app/routers/security.py`
- `backend/app/main.py`
- `frontend/src/App.jsx`
- `frontend/src/services/api.js`
- `frontend/src/styles.css`
- `scripts/backups/backup_postgres.ps1`
- `scripts/backups/restore_postgres.ps1`
- `scripts/backups/README.md`
- `backend/.env.example`

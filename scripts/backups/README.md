# Backup e restauração — MercadoPro

## Backup
No PowerShell, a partir da raiz do projeto:

```powershell
.\scripts\backups\backup_postgres.ps1
```

O script cria um arquivo `.dump` com data/hora. Guarde os backups fora do computador do servidor.

## Restauração

```powershell
.\scripts\backups\restore_postgres.ps1 -BackupFile .\backups\mercadopro_YYYYMMDD_HHMMSS.dump
```

A restauração exige a confirmação `RESTAURAR` e substitui os objetos do banco informado no `backend/.env`.

## Segurança
- Não versionar `backend/.env`.
- Trocar `SECRET_KEY` em produção.
- Alterar a senha demo `admin` antes de colocar o sistema em uso real.
- Testar restaurações periodicamente em uma base separada.

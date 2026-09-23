param([Parameter(Mandatory=$true)][string]$BackupFile)
$ErrorActionPreference = "Stop"
$envFile = Join-Path $PSScriptRoot "..\..\backend\.env"
if (-not (Test-Path $envFile)) { throw "Crie backend\.env antes da restauração." }
$dbLine = Get-Content $envFile | Where-Object { $_ -match '^DATABASE_URL=' } | Select-Object -First 1
$dbUrl = $dbLine.Substring(13).Trim()
if ($dbUrl -match 'postgresql\+psycopg://([^:]+):([^@]+)@([^:/:]+)(?::(\d+))?/([^?]+)') {
  $user=$matches[1]; $pass=$matches[2]; $host=$matches[3]; $port=if($matches[4]){$matches[4]}else{"5432"}; $db=$matches[5]
} else { throw "DATABASE_URL incompatível com o formato esperado." }
$env:PGPASSWORD=$pass
Write-Host "ATENÇÃO: a restauração substitui os dados do banco '$db'."
$confirm = Read-Host "Digite RESTAURAR para continuar"
if ($confirm -ne "RESTAURAR") { Write-Host "Cancelado."; exit 1 }
pg_restore -h $host -p $port -U $user --clean --if-exists --no-owner -d $db $BackupFile
if ($LASTEXITCODE -ne 0) { throw "pg_restore falhou." }
Write-Host "Restauração concluída."

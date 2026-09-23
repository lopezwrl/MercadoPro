param([string]$OutputDir = ".\backups")
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$envFile = Join-Path $PSScriptRoot "..\..\backend\.env"
if (-not (Test-Path $envFile)) { throw "Crie backend\.env antes do backup." }
$envLines = Get-Content $envFile
$dbLine = $envLines | Where-Object { $_ -match '^DATABASE_URL=' } | Select-Object -First 1
if (-not $dbLine) { throw "DATABASE_URL não encontrada." }
$dbUrl = $dbLine.Substring(13).Trim()
if ($dbUrl -match 'postgresql\+psycopg://([^:]+):([^@]+)@([^:/:]+)(?::(\d+))?/([^?]+)') {
  $user=$matches[1]; $pass=$matches[2]; $host=$matches[3]; $port=if($matches[4]){$matches[4]}else{"5432"}; $db=$matches[5]
} else { throw "DATABASE_URL incompatível com o formato esperado." }
$env:PGPASSWORD=$pass
$out = Join-Path $OutputDir "mercadopro_$stamp.dump"
pg_dump -h $host -p $port -U $user -Fc -f $out $db
if ($LASTEXITCODE -ne 0) { throw "pg_dump falhou." }
Write-Host "Backup criado: $out"

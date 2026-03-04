# ════════════════════════════════════════════════════════════════
# SETUP DOCKER + N8N
# Script para instalar Docker y levantar n8n localmente
# ════════════════════════════════════════════════════════════════

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "SETUP: Docker + n8n para SecretarIA" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

# 1. Instalar Docker Desktop
Write-Host "`n[1] Verificando Docker..." -ForegroundColor Yellow
$docker = docker --version 2>$null
if ($docker) {
    Write-Host "✓ Docker ya está instalado: $docker" -ForegroundColor Green
} else {
    Write-Host "✗ Docker no encontrado. Instalando..." -ForegroundColor Red
    winget install Docker.DockerDesktop
    Write-Host "⚠  Docker Desktop instalado. Debes REINICIAR para que funcione." -ForegroundColor Yellow
    exit
}

# 2. Limpiar imagenes viejas
Write-Host "`n[2] Limpiando n8n anterior (si existe)..." -ForegroundColor Yellow
docker stop n8n 2>$null
docker rm n8n 2>$null
Write-Host "✓ Limpieza completada" -ForegroundColor Green

# 3. Crear volumen para persistencia
Write-Host "`n[3] Creando volumen de datos..." -ForegroundColor Yellow
docker volume create n8n_data 2>$null
Write-Host "✓ Volumen creado" -ForegroundColor Green

# 4. Iniciar n8n
Write-Host "`n[4] Iniciando n8n..." -ForegroundColor Yellow
docker run -d `
  --name n8n `
  -p 5678:5678 `
  -v n8n_data:/home/node/.n8n `
  -e N8N_HOST=localhost `
  -e N8N_PORT=5678 `
  -e N8N_PROTOCOL=http `
  n8nio/n8n

Write-Host "✓ n8n iniciado" -ForegroundColor Green

# 5. Esperar a que esté listo
Write-Host "`n[5] Esperando que n8n esté listo (30 segundos)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# 6. Verificar
Write-Host "`n[6] Verificando conectividad..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5678" -TimeoutSec 5 -UseBasicParsing 2>$null
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ n8n está ACTIVO y accesible" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ Esperando más tiempo..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
}

Write-Host "`n═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✓ SETUP COMPLETADO" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "`nAccesible en: http://localhost:5678" -ForegroundColor Cyan
Write-Host "Para parar n8n: docker stop n8n" -ForegroundColor Yellow
Write-Host "Para eliminar:  docker rm n8n" -ForegroundColor Yellow

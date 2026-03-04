#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════
# Test n8n Flujo → Railway API
# ════════════════════════════════════════════════════════════════

import requests
import json
import time
from datetime import datetime

print("=" * 70)
print("TEST: n8n Flujo → Railway API")
print("=" * 70)

# Configuración
N8N_WEBHOOK = "http://localhost:5678/webhook/secretaria"
RAILWAY_API = "https://web-production-a5da.up.railway.app"

# Test data
test_cases = [
    {
        "name": "Test 1: Material simple",
        "data": {
            "constructor_id": "test-001",
            "obra_nombre": "Test",
            "mensaje": "Necesito 50 bolsas de cemento"
        }
    },
    {
        "name": "Test 2: Múltiples materiales",
        "data": {
            "constructor_id": "test-001",
            "obra_nombre": "Test",
            "mensaje": "Necesito 20 kg de clavos, 5 cajas de tornillos y 10 bolsas de arena"
        }
    },
    {
        "name": "Test 3: Marcar comprado",
        "data": {
            "constructor_id": "test-001",
            "obra_nombre": "Test",
            "mensaje": "Ya compré las bolsas de cemento"
        }
    }
]

print("\n[INFO] Verificando conectividad...")

# 1. Verificar n8n
try:
    resp = requests.get("http://localhost:5678", timeout=2)
    print("✓ n8n accesible en localhost:5678")
except Exception as e:
    print(f"✗ ERROR: n8n no está en puerto 5678")
    print(f"   Solución: Ejecuta 'setup_docker_n8n.ps1' primero")
    exit(1)

# 2. Verificar Railway API
try:
    resp = requests.get(f"{RAILWAY_API}/health", timeout=5)
    print("✓ Railway API accesible")
except Exception as e:
    print(f"✗ ERROR: Railway API no responde")
    print(f"   URL: {RAILWAY_API}/health")
    exit(1)

print("\n[TEST] Ejecutando casos de prueba...")
print("-" * 70)

for i, test_case in enumerate(test_cases, 1):
    print(f"\n{test_case['name']}")
    
    try:
        # Enviar webhook request
        resp = requests.post(
            N8N_WEBHOOK,
            json=test_case['data'],
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        # Parsear respuesta
        result = resp.json()
        
        print(f"  Status: {resp.status_code}")
        print(f"  Respuesta: {result.get('respuesta', '')[:80]}...")
        print(f"  Obra ID: {result.get('obra_id', 'N/A')}")
        print(f"  ✓ OK")
        
    except Exception as e:
        print(f"  ✗ ERROR: {str(e)}")

print("\n" + "=" * 70)
print("✓ TEST COMPLETADO")
print("=" * 70)
print("\nPróximos pasos:")
print("1. Webhook creado en n8n")
print("2. HTTP Request conectado a Railway")
print("3. Flujo activo y funcionando")
print("4. Listo para integrar con WATI")

#!/usr/bin/env python3
"""
Test de la API Flask en local
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test del health endpoint"""
    print("1️⃣ TEST /health...")
    try:
        resp = requests.get(f"{BASE_URL}/health")
        print(f"   ✅ Status: {resp.status_code}")
        print(f"   Respuesta: {json.dumps(resp.json(), indent=2)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_mensaje():
    """Test del endpoint /mensaje"""
    print("\n2️⃣ TEST /mensaje...")
    payload = {
        "texto": "necesito 20 bolsas de cemento",
        "constructor_id": "test-api-001",
        "obra_nombre": "Prueba API",
        "historial": []
    }
    try:
        resp = requests.post(f"{BASE_URL}/mensaje", json=payload)
        print(f"   ✅ Status: {resp.status_code}")
        data = resp.json()
        print(f"   Respuesta: {data.get('respuesta')}")
        print(f"   Obra ID: {data.get('obra_id')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_lista():
    """Test del endpoint /lista"""
    print("\n3️⃣ TEST /lista...")
    payload = {
        "constructor_id": "test-api-001",
        "obra_nombre": "Prueba API"
    }
    try:
        resp = requests.post(f"{BASE_URL}/lista", json=payload)
        print(f"   ✅ Status: {resp.status_code}")
        data = resp.json()
        print(f"   Obra ID: {data.get('obra_id')}")
        print(f"   Items: {len(data.get('items', []))} encontrados")
        print(f"   Lista:\n{data.get('lista_texto')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_marcar_comprado():
    """Test de marcar item como comprado"""
    print("\n4️⃣ TEST /mensaje (marcar comprado)...")
    payload = {
        "texto": "marca el 1 como comprado",
        "constructor_id": "test-api-001",
        "obra_nombre": "Prueba API",
        "historial": []
    }
    try:
        resp = requests.post(f"{BASE_URL}/mensaje", json=payload)
        print(f"   ✅ Status: {resp.status_code}")
        data = resp.json()
        print(f"   Respuesta: {data.get('respuesta')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("  TEST API SECRETARIA")
    print("=" * 60)
    print("\n⚠️ Asegúrate de que la API esté corriendo en otra terminal:")
    print("   python api.py")
    print()
    
    input("Presiona Enter cuando esté lista...")
    
    test_health()
    test_mensaje()
    test_lista()
    test_marcar_comprado()
    
    print("\n" + "=" * 60)
    print("✅ TESTS COMPLETADOS")
    print("=" * 60)

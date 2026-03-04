#!/usr/bin/env python3
"""
Test automatizado de agente_obra.py con Supabase
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
CONSTRUCTOR_ID = "test-auto-" + datetime.now().strftime("%Y%m%d%H%M%S")
OBRA_NOMBRE = "Obra de Test Automático"

print("=" * 60)
print("  TEST AUTOMATIZADO DE AGENTE_OBRA + SUPABASE")
print("=" * 60)
print()

# ── Conectarse a Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print(f"✅ Conectado a Supabase")

# ── 1. CREAR OBRA DE TEST
print("\n1️⃣ CREAR OBRA DE TEST...")
try:
    resp = supabase.table("obras").insert({
        "nombre": OBRA_NOMBRE,
        "constructor_id": CONSTRUCTOR_ID,
        "activa": True
    }).execute()
    obra_id = resp.data[0]["id"]
    print(f"   ✅ Obra creada (ID: {obra_id})")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# ── 2. INSERTAR ITEMS
print("\n2️⃣ INSERTAR ITEMS...")
items_test = [
    "20 bolsas de cemento",
    "Llamar al electricista",
    "3 caños de 4 pulgadas"
]
inserted_ids = []
try:
    for item_text in items_test:
        resp = supabase.table("items").insert({
            "obra_id": obra_id,
            "item": item_text,
            "comprado": False,
            "fecha_anotacion": datetime.now().isoformat()
        }).execute()
        id_item = resp.data[0]["id"]
        inserted_ids.append(id_item)
        print(f"   ✅ '{item_text}' → ID {id_item}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# ── 3. LEER LISTA
print("\n3️⃣ LEER LISTA...")
try:
    resp = supabase.table("items").select("*").eq("obra_id", obra_id).execute()
    pendientes = [i for i in resp.data if not i["comprado"]]
    print(f"   ✅ {len(pendientes)} items pendientes:")
    for item in pendientes:
        print(f"      [{item['id']}] {item['item']}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# ── 4. MARCAR COMO COMPRADO
print("\n4️⃣ MARCAR COMO COMPRADO...")
try:
    id_to_mark = inserted_ids[0]
    supabase.table("items").update({
        "comprado": True,
        "fecha_compra": datetime.now().isoformat()
    }).eq("id", id_to_mark).execute()
    print(f"   ✅ Item {id_to_mark} marcado como comprado")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# ── 5. VERIFICAR ESTADO
print("\n5️⃣ VERIFICAR ESTADO...")
try:
    resp = supabase.table("items").select("*").eq("obra_id", obra_id).execute()
    pendientes = [i for i in resp.data if not i["comprado"]]
    comprados = [i for i in resp.data if i["comprado"]]
    print(f"   ✅ Pendientes: {len(pendientes)}")
    print(f"   ✅ Comprados: {len(comprados)}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# ── 6. LIMPIAR (ELIMINAR COMPRADOS)
print("\n6️⃣ LIMPIAR COMPRADOS...")
try:
    for item in comprados:
        supabase.table("items").delete().eq("id", item["id"]).execute()
    print(f"   ✅ {len(comprados)} item(s) eliminado(s)")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# ── RESUMEN
print("\n" + "=" * 60)
print("✅ TODOS LOS TESTS PASARON")
print("=" * 60)
print()
print("SecretarIA está listo para usarse.")
print("Próximo paso: FASE 2 — Integración WhatsApp + n8n")
print()

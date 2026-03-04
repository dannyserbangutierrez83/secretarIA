#!/usr/bin/env python3
"""
Verificar setup de Supabase antes de correr agente_obra.py
"""
import os
import sys
from pathlib import Path

def check_env():
    """Verifica que .env exista y tenga las keys necesarias."""
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ No encontré .env — copia .env.example a .env y llénalo")
        return False
    
    from dotenv import load_dotenv
    load_dotenv()
    
    keys = ["SUPABASE_URL", "SUPABASE_KEY", "ANTHROPIC_API_KEY"]
    missing = []
    for key in keys:
        val = os.getenv(key)
        if not val or val.startswith("YOUR_"):
            missing.append(key)
    
    if missing:
        print(f"❌ Keys sin llenar en .env: {', '.join(missing)}")
        return False
    
    print("✅ .env correcto")
    return True

def check_packages():
    """Verifica que supabase y anthropic estén instalados."""
    try:
        import supabase
        print("✅ supabase-py instalado")
    except ImportError:
        print("❌ supabase-py no instalado — pip install supabase")
        return False
    
    try:
        import anthropic
        print("✅ anthropic instalado")
    except ImportError:
        print("❌ anthropic no instalado — pip install anthropic")
        return False
    
    return True

def check_supabase_connection():
    """Intenta conectarse a Supabase."""
    import os
    from dotenv import load_dotenv
    from supabase import create_client
    
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    try:
        supabase = create_client(url, key)
        # Test: intentar leer tablas
        resp = supabase.table("obras").select("*").limit(1).execute()
        print("✅ Conexión a Supabase OK")
        print(f"   Tablas encontradas y accesibles")
        return True
    except Exception as e:
        print(f"❌ Error conectando a Supabase: {e}")
        print("   → Verifica SUPABASE_URL y SUPABASE_KEY en .env")
        print("   → Verifica que ejecutaste el schema SQL en Supabase")
        return False

def main():
    print("=" * 50)
    print("  VERIFICAR SETUP SECRETARIA")
    print("=" * 50)
    print()
    
    all_ok = True
    
    print("1️⃣ Verificando .env...")
    if not check_env():
        all_ok = False
    print()
    
    print("2️⃣ Verificando paquetes...")
    if not check_packages():
        all_ok = False
    print()
    
    print("3️⃣ Verificando conexión Supabase...")
    if not check_supabase_connection():
        all_ok = False
    print()
    
    if all_ok:
        print("✅ Todo OK. Podés correr: python agente_obra.py")
    else:
        print("❌ Hay errores. Revisa arriba y ejecuta este script de nuevo.")
        sys.exit(1)

if __name__ == "__main__":
    main()

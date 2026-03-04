# 🚀 SETUP SUPABASE — SecretarIA

## PASO 1: Crear proyecto en Supabase

1. Ve a https://supabase.com
2. Sign up / Login
3. New Project
4. Elige:
   - **Name**: SecretarIA
   - **Region**: South America (São Paulo) o cercana a Uruguay
   - **Password**: guarda bien

5. Espera 2-3 min a que se cree

## PASO 2: Ejecutar schema SQL

1. En el dashboard de Supabase, ve a **SQL Editor**
2. New Query
3. Copia todo el contenido de `supabase_schema.sql` de este repo
4. Paste en el editor
5. Click en **Run**
6. Espera confirmación ✅

## PASO 3: Obtener credenciales

1. En Supabase dashboard, ve a **Settings** → **API**
2. Copia:
   - **Project URL** → `SUPABASE_URL`
   - **anon public** key → `SUPABASE_KEY`

## PASO 4: Configurar .env

1. En `c:\Users\Usuario\mi-agente\`, renombra `.env.example` a `.env`
2. Llena:
```
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_KEY=YOUR_ANON_KEY
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
CONSTRUCTOR_ID=dario-obra-001
OBRA_NOMBRE=Obra Principal
```

3. Guarda

## PASO 5: Test

```bash
cd C:\Users\Usuario\mi-agente
venv\Scripts\activate
$env:ANTHROPIC_API_KEY="sk-ant-YOUR_KEY"
python agente_obra.py
```

Prueba escribiendo:
- `necesito 20 bolsas de cemento`
- `qué tengo pendiente`
- `marca el 1 como comprado`

---

## 🔗 RLS (Seguridad — Producción)

El schema incluye Row Level Security. Para DESARROLLO, desactívalo:

```sql
ALTER TABLE obras DISABLE ROW LEVEL SECURITY;
ALTER TABLE items DISABLE ROW LEVEL SECURITY;
```

Ejecútalo en SQL Editor si tienes issues.

---

**Listo cuando termines los 5 pasos.** ↑

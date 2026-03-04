# ════════════════════════════════════════════════════════════════
# CONTEXTO DE SESIÓN — SecretarIA (Continuación)
# Actualizado: Marzo 4, 2026 — Fin de Sesión 1
# ════════════════════════════════════════════════════════════════

## RESUMEN EJECUTIVO

SecretarIA está 60% avanzado. Se completó FASE 1 (Supabase) y FASE 2 (API Flask).
Falta: Deployar en Railway, configurar n8n, conectar WATI.

Repositorio GitHub: https://github.com/dannyserbangutierrez83/secretarIA

---

## ✅ COMPLETADO

### FASE 1: Base de Datos + Agente Local
- ✅ Schema SQL Supabase (obras + items + indexes + RLS)
- ✅ Agente Python con Claude API (guardar_item, ver_lista, marcar_comprado, limpiar_lista)
- ✅ Integración agente_obra.py ↔ Supabase
- ✅ Test CRUD completo (create, read, update, delete funcionan)
- ✅ setup_supabase.md con 5 pasos de config
- ✅ verify_setup.py para validación

**Archivos:**
- `agente_obra.py` — Agente local (CLI)
- `supabase_schema.sql` — DDL Supabase
- `test_supabase.py` — Test CRUD validado ✅
- `.env` — Credenciales (Supabase + Anthropic)

### FASE 2: API Flask
- ✅ API Flask con 3 endpoints:
  - `GET /health` — health check
  - `POST /mensaje` — enviar texto → respuesta IA
  - `POST /lista` — obtener items de obra
- ✅ Integración con agente (tool use funciona)
- ✅ Procfile para Railway
- ✅ requirements.txt generado
- ✅ test_api.py para validar endpoints

**Archivos:**
- `api.py` — Servidor Flask (puerto 5000)
- `Procfile` — Config Railway
- `requirements.txt` — Dependencias
- `test_api.py` — Test HTTP

**Status:** API testeada localmente ✅
- Health check: OK
- /mensaje con Claude: OK
- /lista: OK

### FASE 0: GitHub
- ✅ Repo creado: https://github.com/dannyserbangutierrez83/secretarIA
- ✅ 2 commits pusheados:
  1. "Init: Fase 1 Supabase + agente_obra funcionando"
  2. "Feat: API Flask para SecretarIA - endpoints /mensaje /lista /health"
- ✅ .gitignore configurado (excluye .env, __pycache__, venv)

---

## ⏳ PENDIENTE

### FASE 3: Railway Deployment (NEXT)
**Qué falta:**
1. Crear cuenta en Railway.app
2. Conectar repo GitHub (autorizar)
3. Configurar variables de entorno (SUPABASE_URL, SUPABASE_KEY, ANTHROPIC_API_KEY)
4. Deploy automático
5. Obtener URL pública (https://secretaria-XXXXX.railway.app)

**Archivos listos:** Procfile + requirements.txt + api.py ✅

### FASE 4: n8n Orquestador
**Qué falta:**
1. Levantar n8n en Railway (o editor local)
2. Crear webhook receiver para WATI
3. Crear flujo:
   ```
   WATI Webhook → n8n → POST /mensaje (Railway) → Supabase → Respuesta WhatsApp
   ```
4. Testear flujo end-to-end

**Archivos a crear:**
- `n8n_secretaria_workflow.json` — Flujo exportable

### FASE 5: WATI WhatsApp Gateway
**Qué falta:**
1. Crear cuenta en WATI (wati.io)
2. Obtener API key + Business Phone Number
3. Configurar webhook en WATI → URL de n8n
4. Testear mensaje vía WhatsApp → respuesta

**Documentación a crear:**
- `SETUP_WATI.md` — Pasos de config

---

## 🎯 ARQUITECTURA FINAL

```
Constructor WhatsApp
        ↓
    WATI Gateway (~$50/mes)
        ↓
   n8n en Railway (~$5/mes)
        ↓
   API Flask (Railway)
        ↓
   Claude API (Anthropic)
        ↓
   Supabase (free tier)
        ↓
   Respuesta → WhatsApp
```

---

## 🔐 CREDENCIALES Y KEYS (SEGURIDAD)

**⚠️ NUNCA COMPARTIR EN CHAT:**
- `.env` contiene: SUPABASE_URL, SUPABASE_KEY, ANTHROPIC_API_KEY
- GitHub token usado: [ROTARÁ DESPUÉS — usar el nuevo]
- Supabase key es "anon public" (limitada a tabla policy)

**Para próxima sesión:**
1. Rotar token GitHub (generar uno nuevo en Settings → Developer Settings)
2. Crear Railway API token para CI/CD
3. Generar WATI API key

---

## 📋 PRÓXIMOS PASOS (ORDEN)

### Sesión 2 (Ahora):
1. ✏️ Crear cuenta Railway
2. 🚀 Conectar repo + deploy automático
3. 📝 Verificar que API funciona en Railway
4. 🔄 Generar URL pública de API

### Sesión 3:
1. 📊 Levantar n8n (decisión: Railway vs local)
2. 🔗 Crear webhook + flujo n8n
3. 🧪 Testear flujo completo

### Sesión 4:
1. 💬 Crear cuenta WATI
2. ⚙️ Configurar webhook WATI → n8n
3. 🎉 Primer test con Darío

---

## 🧪 TEST COMMAND REFERENCE

```bash
# Verificar setup local
python verify_setup.py

# Test Supabase CRUD
python test_supabase.py

# Correr API local
python api.py

# Test API (en otra terminal)
python test_api.py

# Verificar git
git status
git log --oneline -5
```

---

## 📦 DEPENDENCIAS INSTALADAS

```
anthropic==0.84.0
Flask==3.1.3
gunicorn==25.1.0
python-dotenv==1.2.2
supabase==2.28.0
requests==2.31.0 (para tests)
```

---

## 🤝 CLIENTE PILOTO

- **Nombre:** Darío
- **Problema:** Se olvida materiales en obra, vuelve 3 veces por día
- **Actual:** Agenda de papel
- **Status:** Ready para demo

---

## 💡 NOTA IMPORTANTE

El modelo de negocio es Land & Expand:
- Setup: $300-500 USD
- Suscripción: $80/$130/$180 USD/mes

Hay +interesados además de Darío.
Production-ready es clave para captar inversión.

---

## 🆘 TROUBLESHOOTING COMMON

| Problema | Solución |
|----------|----------|
| RLS error en Supabase | `ALTER TABLE obras DISABLE ROW LEVEL SECURITY;` en SQL Editor |
| API 500 error | Revisar logs: `venv\Scripts\python api.py` |
| GitHub auth fail | Usar token personal (Settings → Developer Settings → Tokens) |
| Supabase no conecta | Verificar .env tiene SUPABASE_URL y SUPABASE_KEY sin "YOUR_" |

---

## 📞 CONTEXTO DE NEGOCIO

**Ubicación:** Uruguay
**Stack QA anterior:** Java + Selenium (800 casos) + Playwright
**Automatizador:** Abstracta
**Nivel Python:** Básico (scripts)
**Herramienta:** VS Code + Claude Code

**Propuesta:** "El dueño de una pyme opera su negocio hablando, como siempre lo hizo — pero ahora alguien lo escucha, ejecuta y no olvida nada."

---

## ✋ PAUSA AQUÍ

**Próximo paso inmediato:** Railway deployment
- Sesión 2 empieza por crear cuenta Railway
- Setup variables de entorno
- Deploy automático desde GitHub

**Datos para continuación:**
- GitHub: dannyserbangutierrez83/secretarIA
- Supabase Project ID: tizfjnbfqvfyxohzjdpw
- API local testea en puerto 5000

---

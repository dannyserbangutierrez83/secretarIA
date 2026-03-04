# ════════════════════════════════════════════════════════════════
# CONTEXTO DE SESIÓN — SecretarIA (Sesión 2 Completada)
# Actualizado: Marzo 4, 2026 — Fin de Sesión 2
# ════════════════════════════════════════════════════════════════

## RESUMEN EJECUTIVO

SecretarIA está 75% avanzado. Completadas FASES 1, 2 y 3.
✅ Railway deployment funcionando: https://web-production-a5da.up.railway.app/
❌ n8n local: Problemas de instalación (Node.js versión)

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

### FASE 3: Railway Deployment
- ✅ Cuenta Railway creada
- ✅ Repo GitHub conectado (dannyserbangutierrez83/secretarIA)
- ✅ Variables de entorno configuradas:
  - SUPABASE_URL = https://tizfjnbfqvfyxohzjdpw.supabase.co
  - SUPABASE_KEY = sb_publishable_lDJoxrIHrAmQbovrk0RS7A_j07qQ7Nu
  - ANTHROPIC_API_KEY = [configurado]
- ✅ Deploy automático exitoso
- ✅ URL pública: https://web-production-a5da.up.railway.app/
- ✅ Tests en producción: ✅ /health, ✅ /mensaje, ✅ /lista

**Archivos:** api.py + Procfile + requirements.txt ✅

### FASE 0: GitHub
- ✅ Repo creado: https://github.com/dannyserbangutierrez83/secretarIA
- ✅ 2 commits pusheados:
  1. "Init: Fase 1 Supabase + agente_obra funcionando"
  2. "Feat: API Flask para SecretarIA - endpoints /mensaje /lista /health"
- ✅ .gitignore configurado (excluye .env, __pycache__, venv)

---

## ⏳ PENDIENTE

### FASE 4: n8n Orquestador (EN PROGRESO - PROBLEMAS)
**Estado actual:** ❌ Problemas de instalación local
- Node.js actualizado a v24.14.0 ✅
- n8n requiere Node >=20 ✅
- Pero n8n no inicia (posible conflicto de dependencias)

**Alternativas:**
1. **Docker n8n** (recomendado): `docker run -p 5678:5678 n8nio/n8n`
2. **n8n Cloud** (pago): https://n8n.cloud
3. **Railway n8n**: Deploy n8n en Railway (costo ~$5-15/mes)

**Qué falta:**
1. Levantar n8n funcionando
2. Crear webhook receiver para WATI
3. Crear flujo: WATI → n8n → POST /mensaje → Supabase → Respuesta WhatsApp
4. Testear flujo end-to-end

**Archivos a crear:**
- `n8n_secretaria_workflow.json` — Flujo exportable

### FASE 5: WATI WhatsApp Gateway
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

### Sesión 3 (Próxima):
1. 🔧 **Resolver n8n**: Elegir Docker vs Cloud vs Railway
2. 🚀 **Levantar n8n** funcionando en puerto 5678
3. 🔗 **Crear webhook** en n8n para recibir de WATI
4. ⚙️ **Configurar flujo**: WATI → n8n → Railway API → Supabase
5. 🧪 **Test end-to-end**: Simular mensaje WhatsApp

### Sesión 4:
1. 💬 Crear cuenta WATI
2. ⚙️ Configurar webhook WATI → n8n
3. 🎉 Primer test con Darío vía WhatsApp

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

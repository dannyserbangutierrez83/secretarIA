# ════════════════════════════════════════════════════════════════
# CONTEXTO DE SESIÓN — SecretarIA (Sesión 3)
# Actualizado: Marzo 4, 2026 — Inicio de Sesión 3
# ════════════════════════════════════════════════════════════════

## RESUMEN EJECUTIVO

SecretarIA está 75% avanzado. Completadas FASES 1, 2 y 3.
✅ Railway deployment funcionando: https://web-production-a5da.up.railway.app/
❌ n8n local: Problemas de instalación (Node.js versión)

**OBJETIVO SESIÓN 3:** Resolver n8n y crear flujo de integración WATI → n8n → Railway API

Repositorio GitHub: https://github.com/dannyserbangutierrez83/secretarIA

---

## ✅ COMPLETADO (Hasta Sesión 2)

### FASE 1: Base de Datos + Agente Local
- ✅ Schema SQL Supabase (obras + items + indexes + RLS)
- ✅ Agente Python con Claude API (guardar_item, ver_lista, marcar_comprado, limpiar_lista)
- ✅ Integración agente_obra.py ↔ Supabase
- ✅ Test CRUD completo (create, read, update, delete funcionan)
- ✅ setup_supabase.md con 5 pasos de config
- ✅ verify_setup.py para validación

### FASE 2: API Flask
- ✅ API Flask con 3 endpoints:
  - `GET /health` — health check
  - `POST /mensaje` — enviar texto → respuesta IA
  - `POST /lista` — obtener items de obra
- ✅ Integración con agente (tool use funciona)
- ✅ Procfile para Railway
- ✅ requirements.txt generado
- ✅ test_api.py para validar endpoints

### FASE 3: Railway Deployment
- ✅ Cuenta Railway creada
- ✅ Repo GitHub conectado (dannyserbangutierrez83/secretarIA)
- ✅ Variables de entorno configuradas
- ✅ Deploy automático exitoso
- ✅ URL pública: https://web-production-a5da.up.railway.app/
- ✅ Tests en producción: ✅ /health, ✅ /mensaje, ✅ /lista

---

## 🎯 SESIÓN 3: RESOLVER N8N + CREAR FLUJO

### PROBLEMA ACTUAL
- Node.js actualizado a v24.14.0 ✅
- n8n requiere Node >=20 ✅
- Pero n8n no inicia (conflictos de dependencias)

### SOLUCIONES PROPUESTAS
1. **Docker n8n** (recomendado): `docker run -p 5678:5678 n8nio/n8n`
2. **n8n Cloud** (pago): https://n8n.cloud
3. **Railway n8n**: Deploy n8n en Railway

### PLAN DE SESIÓN 3
1. 🔧 **Elegir solución n8n** (Docker recomendado)
2. 🚀 **Levantar n8n** en http://localhost:5678
3. 🔗 **Crear webhook** en n8n para WATI
4. ⚙️ **Configurar flujo**:
   ```
   Webhook (WATI) → HTTP Request → Railway API (/mensaje) → Supabase → Respuesta
   ```
5. 🧪 **Test end-to-end** con Postman/curl

### ARCHIVOS A CREAR
- `n8n_secretaria_workflow.json` — Flujo exportable
- `test_n8n_flow.py` — Script para testear flujo

---

## 🔗 ENDPOINTS DISPONIBLES

**Railway API (Producción):**
- `GET https://web-production-a5da.up.railway.app/health`
- `POST https://web-production-a5da.up.railway.app/mensaje`
- `POST https://web-production-a5da.up.railway.app/lista`

**Formato /mensaje:**
```json
{
  "constructor_id": "dario-obra-001",
  "obra_nombre": "Obra Principal",
  "texto": "Necesito 20 bolsas de cemento y 5 kg de clavos"
}
```

---

## 📋 CHECKLIST SESIÓN 3

- [ ] Instalar Docker (si eliges Docker n8n)
- [ ] Levantar n8n: `docker run -p 5678:5678 n8nio/n8n`
- [ ] Acceder a http://localhost:5678
- [ ] Crear webhook node en n8n
- [ ] Configurar HTTP Request node → Railway API
- [ ] Testear flujo con Postman
- [ ] Exportar workflow como JSON

---

## 🎯 PRÓXIMA SESIÓN 4: WATI INTEGRATION

Una vez n8n funcionando:
1. Crear cuenta WATI (wati.io)
2. Configurar webhook WATI → URL de n8n
3. Test real con WhatsApp de Darío

---

## 🆘 TROUBLESHOOTING N8N

| Problema | Solución |
|----------|----------|
| Docker no instalado | `winget install Docker.DockerDesktop` |
| Puerto 5678 ocupado | Cambiar a `-p 8080:5678` |
| n8n no inicia | Ver logs: `docker logs <container_id>` |
| Webhook no recibe | Verificar URL en n8n (http://localhost:5678) |

---

## 💡 NOTA IMPORTANTE

**Elección n8n:**
- **Docker**: Gratis, local, más control
- **Cloud**: $20/mes, sin instalación, siempre disponible
- **Railway**: $5-15/mes, mismo hosting que API

**Recomendación:** Empezar con Docker para testing rápido.

---

## 📞 CONTEXTO DE NEGOCIO

- **Cliente:** Darío (constructor uruguayo)
- **Problema:** Se olvida materiales en obra
- **Solución:** WhatsApp + IA que nunca olvida
- **Stack:** WhatsApp → WATI → n8n → Railway → Claude → Supabase

**Progreso:** 75% completado. Faltan 2 semanas para demo con cliente real.

---
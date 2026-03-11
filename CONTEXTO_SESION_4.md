# CONTEXTO SESION 4 — SecretarIA
# Fecha: Marzo 5, 2026

## ESTADO ACTUAL

**Progreso:** 90% completado.

### COMPLETADO HOY (Sesion 4):
- n8n deployado en Railway: https://n8n-production-3377.up.railway.app
- Workflow importado desde local y publicado en Railway
- Test exitoso con PowerShell a URL publica (200 OK)
- WATI cuenta paga activa (plan basico)

### PROXIMO PASO INMEDIATO:
Configurar webhook en WATI apuntando a n8n en Railway.
Luego agregar nodo en n8n para responder via WATI API.

---

## ARQUITECTURA COMPLETA

```
Dario (WhatsApp) -> WATI -> n8n (Railway) -> Railway API -> Claude -> Supabase
                                                  |
                                            responde via WATI API -> Dario
```

---

## URLS Y CREDENCIALES CLAVE

**Railway API (produccion):**
- GET  https://web-production-a5da.up.railway.app/health
- POST https://web-production-a5da.up.railway.app/mensaje
- POST https://web-production-a5da.up.railway.app/lista

**n8n Railway (produccion):**
- Dashboard: https://n8n-production-3377.up.railway.app
- Webhook URL: https://n8n-production-3377.up.railway.app/webhook/secretaria-webhook

**WATI:**
- Dashboard: https://live.wati.io/10107400/login
- Cuenta paga activa

---

## N8N WORKFLOW (activo en Railway)

**Nodo 1: Webhook**
- Method: POST
- Path: secretaria-webhook
- Respond: Immediately

**Nodo 2: HTTP Request**
- Method: POST
- URL: https://web-production-a5da.up.railway.app/mensaje
- Body fields:
  - constructor_id: `{{ $json["constructor_id"] }}` (corchetes — palabra reservada JS)
  - obra_nombre: `{{ $json.body.obra_nombre }}`
  - texto: `{{ $json.body.texto }}`

---

## PLAN PROXIMA SESION

1. Configurar webhook en WATI:
   - URL: https://n8n-production-3377.up.railway.app/webhook/secretaria-webhook
   - Evento: Mensaje Recibido
2. Obtener API token de WATI (Settings -> API)
3. Agregar nodo HTTP Request en n8n para responder via WATI API
4. Mapear numero de telefono -> constructor_id (para identificar quien escribe)
5. Probar flujo completo WhatsApp -> respuesta en WhatsApp

---

## WATI API (para responder mensajes)

Para que n8n responda al usuario via WATI, el nodo HTTP Request necesita:
- Method: POST
- URL: `https://live.wati.io/10107400/api/v1/sendSessionMessage/{whatsapp_number}`
- Header: `Authorization: Bearer {API_TOKEN}`
- Body: `{ "messageText": "respuesta de Claude" }`

El numero de telefono del usuario llega en el webhook de WATI en el campo `waId` o `from`.

---

## STACK COMPLETO

- **Supabase:** Schema obras + items, CRUD funcionando (free tier)
- **agente_obra.py:** Agente Python con Claude API (tool use)
- **api.py:** Flask API con /health /mensaje /lista
- **Railway:** API + n8n deployados y funcionando
- **n8n:** Railway, workflow activo, URL publica
- **WATI:** Cuenta paga activa, webhook pendiente de configurar
- **GitHub:** https://github.com/dannyserbangutierrez83/secretarIA

---

## VISIÓN DEL PRODUCTO

**SecretarIA** — Secretaria virtual para constructores via WhatsApp
- Mercado: albañiles y constructores desorganizados
- Canal: WhatsApp (sin friccion, ya lo usan)
- Precio: $30-50/mes basico, $80-100/mes pro
- Costos fijos: ~$75-85/mes
- Break even: 1 usuario a $100/mes

**Roadmap:**
- MVP: Lista materiales + historial (CASI LISTO)
- Corto: Multiples usuarios con sus propias obras
- Mediano: Presupuestos PDF, envio de emails
- Largo: Llamadas automaticas, reportes, proveedores

## CONTEXTO DE NEGOCIO
- Cliente demo: Dario (constructor uruguayo)
- GitHub: https://github.com/dannyserbangutierrez83/secretarIA

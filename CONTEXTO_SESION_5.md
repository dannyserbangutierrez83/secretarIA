# CONTEXTO SESION 5 — SecretarIA
# Fecha: Marzo 9, 2026

## ESTADO ACTUAL

**Progreso:** MVP COMPLETO ✓

### COMPLETADO (Sesion 5):
- Migrado de WATI/WhatsApp a Telegram (WATI no habilitó el teléfono)
- Bot de Telegram creado
- n8n workflow reconstruido con Telegram Trigger
- Flujo completo funcionando end-to-end

### FLUJO COMPLETO (funcionando):
```
Usuario (Telegram) → n8n (Railway) → Railway API → Claude → Supabase
                                                        ↓
                                          responde via Telegram bot
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

**Telegram:**
- Bot creado y funcionando
- Webhook registrado manualmente en Telegram apuntando a n8n

**Variable Railway n8n:**
- WEBHOOK_URL=https://n8n-production-3377.up.railway.app/  (con barra final)

---

## N8N WORKFLOW (activo)

**Nodo 1: Telegram Trigger**
- Updates: message

**Nodo 2: HTTP Request**
- Method: POST
- URL: https://web-production-a5da.up.railway.app/mensaje
- Body: texto, constructor_id (chat.id), obra_nombre

**Nodo 3: Merge**
- Combina Telegram Trigger + HTTP Request
- Necesario para acceder al chat.id en el nodo final

**Nodo 4: Telegram (send)**
- Chat ID: message.chat.id (del Trigger via Merge)
- Text: campo `respuesta` de la Railway API

---

## PROXIMOS PASOS

1. **Voz (próxima sesión):**
   - Crear cuenta en Groq (console.groq.com) y obtener API key
   - Agregar en n8n: detectar mensaje de voz → descargar audio → Groq Whisper → transcribir → Railway API
   - Groq elegido sobre OpenAI por costo ($0.02/hora de audio vs más caro)
2. Mapear numero de Telegram → constructor_id real (base de datos)
3. Manejo de multiples usuarios/obras
4. Comandos especiales (/lista, /nueva_obra, etc.)
5. Presupuestos PDF
6. Conseguir primer cliente (Dario u otro constructor)

---

## STACK COMPLETO

- **Supabase:** Schema obras + items, CRUD funcionando
- **agente_obra.py:** Agente Python con Claude API (tool use)
- **api.py:** Flask API con /health /mensaje /lista
- **Railway:** API + n8n deployados y funcionando
- **n8n:** Workflow activo con Telegram Trigger
- **Telegram:** Bot funcionando (reemplazó a WATI)
- **GitHub:** https://github.com/dannyserbangutierrez83/secretarIA

---

## VISIÓN DEL PRODUCTO

**SecretarIA** — Secretaria virtual para constructores via Telegram
- Mercado: albañiles y constructores desorganizados
- Canal: Telegram (gratis, sin fricción)
- Precio: $30-50/mes basico, $80-100/mes pro
- Costos fijos: ~$75-85/mes
- Break even: 1 usuario a $100/mes

**Roadmap:**
- MVP: Lista materiales + historial ✓ LISTO
- Corto: Multiples usuarios con sus propias obras
- Mediano: Presupuestos PDF, comandos especiales
- Largo: Llamadas automaticas, reportes, proveedores

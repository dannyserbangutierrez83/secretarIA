# CONTEXTO SESION 8 — SecretarIA
# Fecha: Marzo 13, 2026

## ESTADO ACTUAL

**Progreso:** MVP completo y funcionando en producción ✅

### COMPLETADO (Sesion 8):
- Deploy completo: GitHub ✅ | Railway ✅ | Supabase migrado ✅
- Usuario insertado en tabla `usuarios` (telegram_id: 936694100)
- Historial de conversación implementado (tabla `mensajes`, últimos 10 por usuario+obra)
- Cantidades parciales implementadas (`cantidad_total`, `cantidad_pendiente` en tabla `items`)
- IDs ocultos al usuario (solo uso interno del agente)
- Probado y funcionando: referencias en contexto, compras parciales, ambigüedad, memoria entre turnos

### FEATURES ACTIVAS EN PRODUCCIÓN:
1. Múltiples obras por usuario (máx 5) con comandos /obras /nueva /cambiar /ayuda
2. Autenticación por telegram_id
3. Historial de conversación por usuario+obra
4. Cantidades con descuento parcial
5. Manejo de ambigüedad (pide aclaración antes de actuar)

---

## SCHEMA SUPABASE (actual, completo)

```
usuarios
├── telegram_id  TEXT  (PK)
├── nombre       TEXT
├── activo       BOOL  default true
├── obra_activa_id  BIGINT → obras.id
└── created_at

obras
├── id           BIGSERIAL (PK)
├── nombre       TEXT
├── constructor_id  TEXT → usuarios.telegram_id
└── creada_en

items
├── id                BIGSERIAL (PK)
├── obra_id           BIGINT → obras.id
├── item              TEXT
├── comprado          BOOL
├── fecha_anotacion   TIMESTAMPTZ
├── fecha_compra      TIMESTAMPTZ
├── cantidad_total    NUMERIC (nullable)
└── cantidad_pendiente NUMERIC (nullable)

mensajes
├── id          BIGSERIAL (PK)
├── telegram_id TEXT
├── obra_id     BIGINT
├── role        TEXT  ('user' | 'assistant')
├── content     TEXT
└── created_at  TIMESTAMPTZ
```

---

## HERRAMIENTAS DEL AGENTE (api.py)

| Herramienta | Cuándo la usa |
|---|---|
| `guardar_item(item, cantidad?)` | Algo nuevo que necesita comprar/hacer |
| `ver_lista` | Pregunta qué tiene pendiente |
| `marcar_comprado(ids)` | Compró TODO de un item |
| `actualizar_cantidad(id, cantidad_comprada)` | Compró UNA PARTE de un item |
| `limpiar_lista` | Pide limpiar los ya comprados |

---

## URLS Y CREDENCIALES CLAVE

**Railway API (produccion):**
- GET  https://web-production-a5da.up.railway.app/health
- POST https://web-production-a5da.up.railway.app/mensaje
- POST https://web-production-a5da.up.railway.app/lista

**n8n Railway (produccion):**
- Dashboard: https://n8n-production-3377.up.railway.app
- Webhook URL: https://n8n-production-3377.up.railway.app/webhook/secretaria-webhook

**Supabase:** https://supabase.com/dashboard/project/tizfjnbfqvfyxohzjdpw
**GitHub:** https://github.com/dannyserbangutierrez83/secretarIA

---

## ROADMAP

1. **Voz (Groq)** — transcribir audios de Telegram. Seguir SETUP_VOZ_GROQ.md. Necesita API key de console.groq.com
2. **calcular_materiales** — herramienta que calcula cuánto cemento/arena/etc. necesitás por m2
3. **registrar_gasto** — seguimiento de costos por obra
4. **Presupuestos PDF** — generar y mandar al cliente
5. **Primer cliente real** — onboardear a Dario u otro constructor

---

## VISIÓN DEL PRODUCTO

**SecretarIA** — Secretaria virtual para constructores via Telegram
- Mercado: albañiles y constructores desorganizados
- Canal: Telegram (gratis, sin fricción)
- Precio: $30-50/mes básico, $80-100/mes pro
- Costos fijos: ~$75-85/mes
- Break even: 1 usuario a $100/mes
- Ventaja competitiva: habla como uruguayo de obra, entiende el contexto local

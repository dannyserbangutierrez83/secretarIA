# CONTEXTO SESION 6 — SecretarIA
# Fecha: Marzo 10, 2026

## ESTADO ACTUAL

**Progreso:** MVP + múltiples obras ✓ (pendiente deploy)

### COMPLETADO (Sesion 6):
- `api.py` actualizado con autenticación y múltiples obras
- `migracion_multiples_obras.sql` listo para ejecutar en Supabase
- `SETUP_VOZ_GROQ.md` documentación lista para cuando llegue la API key
- Código optimizado (N+1 eliminados, queries batch)

### PENDIENTE (próxima sesión o cuando haya tiempo):
1. `git push origin main` → Railway redeploya automático (~2 min)
2. Ejecutar `migracion_multiples_obras.sql` en Supabase SQL Editor
3. Mandar mensaje al bot → ver telegram_id en logs de Railway
4. `INSERT INTO usuarios (telegram_id, nombre) VALUES ('ID', 'Nombre');`

---

## FLUJO COMPLETO (funcionando en código, pendiente deploy)

```
Usuario (Telegram) → n8n (Railway) → Railway API → Claude → Supabase
                                           ↓
                                    autenticación (tabla usuarios)
                                    comandos /obras /nueva /cambiar /ayuda
                                    hasta 5 obras por constructor
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

**GitHub:** https://github.com/dannyserbangutierrez83/secretarIA

---

## SCHEMA SUPABASE (post-migración)

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

items  (sin cambios)
├── id, obra_id, item, comprado, fecha_anotacion, fecha_compra
```

---

## COMANDOS DISPONIBLES (en el bot)

| Comando | Acción |
|---------|--------|
| `/obras` | Lista todas las obras del usuario |
| `/nueva Casa Playa` | Crea obra nueva y la activa (máx 5) |
| `/cambiar 2` | Cambia la obra activa por número |
| `/ayuda` | Muestra los comandos disponibles |
| (texto normal) | Va a Claude con la obra activa |

---

## PRÓXIMOS PASOS (roadmap)

1. **Deploy pendiente** — push + SQL + insertar usuario (ver arriba)
2. **Voz (Groq)** — crear cuenta en console.groq.com, seguir SETUP_VOZ_GROQ.md
3. **Primer cliente** — probar con Dario u otro constructor
4. **Presupuestos PDF**
5. **Múltiples constructores con sus propias obras** (ya está el código)

---

## STACK COMPLETO

- **Supabase:** obras + items + usuarios, CRUD funcionando
- **api.py:** Flask + Claude API (tool use) + auth + múltiples obras
- **Railway:** API + n8n deployados
- **n8n:** Workflow activo con Telegram Trigger
- **Telegram:** Bot funcionando
- **GitHub:** https://github.com/dannyserbangutierrez83/secretarIA

---

## VISIÓN DEL PRODUCTO

**SecretarIA** — Secretaria virtual para constructores via Telegram
- Mercado: albañiles y constructores desorganizados
- Canal: Telegram (gratis, sin fricción)
- Precio: $30-50/mes basico, $80-100/mes pro
- Costos fijos: ~$75-85/mes
- Break even: 1 usuario a $100/mes

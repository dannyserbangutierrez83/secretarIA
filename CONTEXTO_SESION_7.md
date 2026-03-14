# CONTEXTO SESION 7 — SecretarIA
# Fecha: Marzo 13, 2026

## ESTADO ACTUAL

**Progreso:** MVP + múltiples obras ✓ | GitHub en sync ✓ | Railway deploy pendiente confirmación

### COMPLETADO (Sesion 7):
- Confirmado que GitHub ya está actualizado (git push → "Everything up-to-date")
- Railway tiene el código más reciente (redeploy automático al push)
- Discusión estratégica: arquitectura de agentes (ver abajo)
- Decisión: implementar historial de conversación (memoria de charla)

### PENDIENTE INMEDIATO:
1. Ejecutar `migracion_multiples_obras.sql` en Supabase SQL Editor
2. Mandar mensaje al bot → ver telegram_id en logs de Railway
3. `INSERT INTO usuarios (telegram_id, nombre) VALUES ('ID', 'Nombre');`
4. **Implementar historial de conversación** (próxima tarea de código)

---

## PRÓXIMA FEATURE: HISTORIAL DE CONVERSACIÓN

### Plan técnico:
- Nueva tabla en Supabase:
```sql
CREATE TABLE mensajes (
    id          BIGSERIAL PRIMARY KEY,
    telegram_id TEXT NOT NULL,
    obra_id     BIGINT NOT NULL,
    role        TEXT NOT NULL,  -- 'user' o 'assistant'
    content     TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
```
- Modificar `procesar_mensaje` en `api.py` para:
  1. Cargar últimos ~10 mensajes del usuario+obra al inicio
  2. Guardar mensaje del usuario y respuesta del asistente al final
- Scope: por `telegram_id + obra_id` (cada obra tiene su propio hilo)
- Límite: últimos 10 mensajes (~5 turnos) para controlar tokens

### Por qué vale la pena:
Sin historial, el agente no entiende referencias como "ya compré las primeras 3".
Con historial, las conversaciones son naturales y el agente recuerda contexto.

---

## DECISIONES ESTRATÉGICAS (Sesion 7)

**Arquitectura de agentes:** Un solo agente con múltiples herramientas (NO orquestador, NO múltiples agentes separados).
- El albañil quiere hablar con UNA cosa
- Claude ya hace el routing interno con tool use
- El orquestador es complejidad innecesaria en esta etapa

**Ventaja competitiva:** No competir con empresas grandes en agentes genéricos.
Apostar a: habla como uruguayo de obra, conoce contexto local, entiende al albañil.

**Próximas herramientas de mayor valor:**
1. `calcular_materiales(tipo, m2)` — evita comprar de más/menos
2. `registrar_gasto(monto, descripcion)` — seguimiento de costos por obra
3. `generar_presupuesto(items)` — PDF/texto para mandar al cliente

---

## FLUJO COMPLETO

```
Usuario (Telegram) → n8n (Railway) → Railway API → Claude → Supabase
                                           ↓
                                    autenticación (tabla usuarios)
                                    comandos /obras /nueva /cambiar /ayuda
                                    hasta 5 obras por constructor
                                    historial de conversación (próximo)
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

## SCHEMA SUPABASE (post-migración pendiente)

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
├── id, obra_id, item, comprado, fecha_anotacion, fecha_compra

mensajes  ← PENDIENTE CREAR
├── id, telegram_id, obra_id, role, content, created_at
```

---

## STACK COMPLETO

- **Supabase:** obras + items + usuarios, CRUD funcionando
- **api.py:** Flask + Claude API (tool use) + auth + múltiples obras
- **Railway:** API + n8n deployados
- **n8n:** Workflow activo con Telegram Trigger
- **Telegram:** Bot funcionando
- **GitHub:** https://github.com/dannyserbangutierrez83/secretarIA

---

## ROADMAP

1. **Deploy completo** — SQL migration + insertar usuario (pendiente)
2. **Historial de conversación** — tabla mensajes + modificar procesar_mensaje
3. **Voz (Groq)** — crear cuenta en console.groq.com, seguir SETUP_VOZ_GROQ.md
4. **Primer cliente** — probar con Dario u otro constructor
5. **calcular_materiales** — herramienta de mayor valor inmediato
6. **registrar_gasto** — seguimiento de costos
7. **Presupuestos PDF**

---

## VISIÓN DEL PRODUCTO

**SecretarIA** — Secretaria virtual para constructores via Telegram
- Mercado: albañiles y constructores desorganizados
- Canal: Telegram (gratis, sin fricción)
- Precio: $30-50/mes basico, $80-100/mes pro
- Costos fijos: ~$75-85/mes
- Break even: 1 usuario a $100/mes

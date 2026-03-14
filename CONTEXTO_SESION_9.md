# CONTEXTO SESION 9 — SecretarIA
# Fecha: Marzo 13, 2026

## ESTADO ACTUAL

**Progreso:** MVP robusto funcionando en producción ✅

### COMPLETADO (Sesion 9):
- `registrar_gasto(descripcion, monto, categoria?)` — guarda gastos por obra
- `ver_gastos(periodo?)` — resumen con filtro: hoy / semana / mes / total
- Tabla `gastos` creada en Supabase
- Probado y funcionando en Telegram

### FEATURES ACTIVAS EN PRODUCCIÓN:
1. Múltiples obras por usuario (máx 5) — /obras /nueva /cambiar /ayuda
2. Autenticación por telegram_id
3. Historial de conversación por usuario+obra (últimos 10 mensajes)
4. Cantidades con descuento parcial
5. Manejo de ambigüedad (pide aclaración antes de actuar)
6. Cálculo de materiales por tipo y medida (Claude como motor)
7. Registro y consulta de gastos por período

---

## HERRAMIENTAS DEL AGENTE (api.py)

| Herramienta | Cuándo la usa |
|---|---|
| `guardar_item(item, cantidad?)` | Algo nuevo que necesita comprar/hacer |
| `ver_lista` | Pregunta qué tiene pendiente |
| `marcar_comprado(ids)` | Compró TODO de un item |
| `actualizar_cantidad(id, cantidad_comprada)` | Compró UNA PARTE de un item |
| `calcular_materiales(tipo, medidas, aclaraciones?)` | Cuánto material necesita para un trabajo |
| `registrar_gasto(descripcion, monto, categoria?)` | Gastó plata en algo |
| `ver_gastos(periodo?)` | Cuánto llevo gastado (hoy/semana/mes/total) |
| `limpiar_lista` | Limpiar items ya comprados |

---

## SCHEMA SUPABASE (completo y actualizado)

```
usuarios
├── telegram_id, nombre, activo, obra_activa_id, created_at

obras
├── id, nombre, constructor_id, creada_en

items
├── id, obra_id, item, comprado, fecha_anotacion, fecha_compra
├── cantidad_total (nullable), cantidad_pendiente (nullable)

mensajes
├── id, telegram_id, obra_id, role, content, created_at

gastos
├── id, obra_id, telegram_id, descripcion, monto, categoria, created_at
```

---

## URLS Y CREDENCIALES CLAVE

**Railway API:** https://web-production-a5da.up.railway.app
**n8n Webhook:** https://n8n-production-3377.up.railway.app/webhook/secretaria-webhook
**Supabase:** https://supabase.com/dashboard/project/tizfjnbfqvfyxohzjdpw
**GitHub:** https://github.com/dannyserbangutierrez83/secretarIA

---

## ROADMAP

1. **Contactos** — guardar teléfonos de proveedores y llamarlos por nombre
2. **Voz (Groq)** — transcribir audios de Telegram. Seguir SETUP_VOZ_GROQ.md
3. **Recordatorios** — "avisame mañana a las 8"
4. **Registrar medidas** — "la pared norte mide 8.40m" para no ir a ver de vuelta
5. **Presupuestos PDF** — generar y mandar al cliente
6. **Primer cliente real** — onboardear a Dario u otro constructor

---

## VISIÓN DEL PRODUCTO

**SecretarIA** — Secretaria virtual para constructores via Telegram
- Mercado: albañiles y constructores desorganizados
- Canal: Telegram (gratis, sin fricción)
- Precio: $30-50/mes básico, $80-100/mes pro
- Costos fijos: ~$75-85/mes
- Break even: 1 usuario a $100/mes
- Ventaja competitiva: habla como uruguayo de obra, entiende el contexto local

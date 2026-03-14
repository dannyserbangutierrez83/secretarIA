# CONTEXTO SESION 10 — SecretarIA
# Fecha: Marzo 14, 2026

## ESTADO ACTUAL

**Progreso:** MVP robusto con 7 herramientas ✅ | Seguridad API_SECRET implementada ⚠️ (debugging pendiente)

### COMPLETADO (Sesion 9-10):
- `registrar_gasto` y `ver_gastos` funcionando en producción
- Tabla `gastos` en Supabase
- Código de seguridad `API_SECRET` implementado en `api.py`
- Variable `API_SECRET=s2cr2t1rIAs2cr2t1rIA` configurada en Railway
- Header `X-API-Secret` configurado en n8n (Using Fields Below)

### PROBLEMA PENDIENTE — API_SECRET:
- El bot dejó de responder después de configurar el secret
- Railway no muestra logs → el request no llega desde n8n
- n8n muestra: "Authorization failed - please check your credentials"
- Authentication en el nodo HTTP Request está en **None**
- El valor del secret es idéntico en Railway y n8n

**Posibles causas a investigar:**
1. n8n tiene alguna autenticación propia activada en otro lugar del nodo
2. El workflow de n8n se desactivó al editarlo
3. Problema de redeploy en Railway — probar forzar redeploy
4. **Solución temporal:** sacar `API_SECRET` de Railway para volver a funcionar, debuggear después

---

## FEATURES ACTIVAS EN PRODUCCIÓN

1. Múltiples obras por usuario (máx 5) — /obras /nueva /cambiar /ayuda
2. Autenticación por telegram_id
3. Historial de conversación por usuario+obra (últimos 10 mensajes)
4. Cantidades con descuento parcial
5. Manejo de ambigüedad
6. Cálculo de materiales por tipo y medida
7. Registro y consulta de gastos por período

---

## HERRAMIENTAS DEL AGENTE (api.py)

| Herramienta | Cuándo la usa |
|---|---|
| `guardar_item(item, cantidad?)` | Algo nuevo que necesita comprar/hacer |
| `ver_lista` | Pregunta qué tiene pendiente |
| `marcar_comprado(ids)` | Compró TODO de un item |
| `actualizar_cantidad(id, cantidad_comprada)` | Compró UNA PARTE de un item |
| `calcular_materiales(tipo, medidas, aclaraciones?)` | Cuánto material necesita |
| `registrar_gasto(descripcion, monto, categoria?)` | Gastó plata en algo |
| `ver_gastos(periodo?)` | Cuánto llevo gastado (hoy/semana/mes/total) |
| `limpiar_lista` | Limpiar items ya comprados |

---

## SCHEMA SUPABASE (completo)

```
usuarios    — telegram_id, nombre, activo, obra_activa_id, created_at
obras       — id, nombre, constructor_id, creada_en
items       — id, obra_id, item, comprado, fecha_anotacion, fecha_compra, cantidad_total, cantidad_pendiente
mensajes    — id, telegram_id, obra_id, role, content, created_at
gastos      — id, obra_id, telegram_id, descripcion, monto, categoria, created_at
```

---

## URLS Y CREDENCIALES CLAVE

**Railway API:** https://web-production-a5da.up.railway.app
**n8n Webhook:** https://n8n-production-3377.up.railway.app/webhook/secretaria-webhook
**Supabase:** https://supabase.com/dashboard/project/tizfjnbfqvfyxohzjdpw
**GitHub:** https://github.com/dannyserbangutierrez83/secretarIA

---

## ROADMAP

1. **Resolver API_SECRET** — debuggear o temporalmente desactivar para restaurar servicio
2. **Contactos** — guardar teléfonos de proveedores
3. **Voz (Groq)** — transcribir audios de Telegram
4. **Recordatorios** — "avisame mañana a las 8"
5. **Registrar medidas** — "la pared norte mide 8.40m"
6. **Presupuestos PDF**
7. **Primer cliente real** — onboardear a Dario u otro constructor

---

## VISIÓN DEL PRODUCTO

**SecretarIA** — Secretaria virtual para constructores via Telegram
- Mercado: albañiles y constructores desorganizados
- Canal: Telegram (gratis, sin fricción)
- Precio: $30-50/mes básico, $80-100/mes pro
- Costos fijos: ~$75-85/mes
- Break even: 1 usuario a $100/mes
- Ventaja competitiva: habla como uruguayo de obra, entiende el contexto local

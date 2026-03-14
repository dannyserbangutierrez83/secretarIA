# CONTEXTO SESION 11 — SecretarIA
# Fecha: Marzo 14, 2026

## ESTADO ACTUAL

**Progreso:** MVP robusto con 9 herramientas ✅ | Seguridad API_SECRET pendiente de debug ⚠️

### COMPLETADO (Sesion 11):
- `guardar_contacto`, `ver_contactos`, `eliminar_contacto` — tabla `contactos` en Supabase
- Contactos son **por usuario** (no por obra) — disponibles en todas las obras
- `eliminar_contacto` requiere confirmación explícita (parámetro `confirmar=false/true`)
- Protección: nunca borra todos los contactos a la vez

### PROBLEMA PENDIENTE — API_SECRET:
- El bot dejó de responder después de configurar el secret
- Railway no muestra logs → el request no llega desde n8n
- n8n muestra: "Authorization failed - please check your credentials"
- Ver CONTEXTO_SESION_10.md para detalles

---

## FEATURES ACTIVAS EN PRODUCCIÓN

1. Múltiples obras por usuario (máx 5) — /obras /nueva /cambiar /ayuda
2. Autenticación por telegram_id
3. Historial de conversación por usuario+obra (últimos 10 mensajes)
4. Cantidades con descuento parcial
5. Manejo de ambigüedad
6. Cálculo de materiales por tipo y medida
7. Registro y consulta de gastos por período
8. Contactos/proveedores (guardar, ver, eliminar con confirmación)

---

## HERRAMIENTAS DEL AGENTE (api.py) — 9 tools

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
| `guardar_contacto(nombre, telefono, rubro?)` | Guardar proveedor/contacto |
| `ver_contactos(rubro?)` | Ver proveedores, filtrable por rubro |
| `eliminar_contacto(nombre, confirmar)` | Borrar contacto con confirmación |

---

## SCHEMA SUPABASE (completo)

```
usuarios    — telegram_id, nombre, activo, obra_activa_id, created_at
obras       — id, nombre, constructor_id, creada_en
items       — id, obra_id, item, comprado, fecha_anotacion, fecha_compra, cantidad_total, cantidad_pendiente
mensajes    — id, telegram_id, obra_id, role, content, created_at
gastos      — id, obra_id, telegram_id, descripcion, monto, categoria, created_at
contactos   — id, constructor_id, nombre, telefono, rubro, created_at
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
2. **Voz (Groq)** — transcribir audios de Telegram
3. **Recordatorios** — "avisame mañana a las 8"
4. **Registrar medidas** — "la pared norte mide 8.40m"
5. **Presupuestos PDF**
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

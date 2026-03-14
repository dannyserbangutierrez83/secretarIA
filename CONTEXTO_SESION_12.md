# CONTEXTO SESION 12 — SecretarIA
# Fecha: Marzo 14, 2026

## ESTADO ACTUAL

**Progreso:** MVP robusto con 12 herramientas ✅ | Seguridad API_SECRET pendiente de debug ⚠️

### COMPLETADO (Sesion 12):
- **Contactos:** `guardar_contacto`, `ver_contactos`, `eliminar_contacto` (con confirmación, nunca borra todos)
- **Presupuestos PDF:** `agregar_linea_presupuesto`, `ver_presupuesto`, `quitar_linea_presupuesto`
- Endpoint `/presupuesto/pdf` genera PDF con reportlab y lo devuelve como archivo
- Claude responde `[GENERAR_PDF]` → n8n detecta con IF contains → llama endpoint → manda PDF por Telegram
- **Bug resuelto:** nodo IF en n8n tenía que usar "contains" (no "equals")

### PROBLEMA PENDIENTE — API_SECRET:
- El bot dejó de responder después de configurar el secret
- Ver CONTEXTO_SESION_10.md para detalles
- Solución temporal: API_SECRET no está activo en producción

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
9. Presupuestos PDF (armar líneas, generar y enviar por Telegram)

---

## HERRAMIENTAS DEL AGENTE (api.py) — 12 tools

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
| `agregar_linea_presupuesto(descripcion, cantidad, unidad, precio_unitario)` | Agregar línea al presupuesto |
| `ver_presupuesto()` | Ver presupuesto con desglose y total |
| `quitar_linea_presupuesto(descripcion, confirmar)` | Quitar línea con confirmación |

> Nota: Claude responde `[GENERAR_PDF]` para disparar el PDF — no es un tool sino un trigger para n8n.

---

## SCHEMA SUPABASE (completo)

```
usuarios           — telegram_id, nombre, activo, obra_activa_id, created_at
obras              — id, nombre, constructor_id, creada_en
items              — id, obra_id, item, comprado, fecha_anotacion, fecha_compra, cantidad_total, cantidad_pendiente
mensajes           — id, telegram_id, obra_id, role, content, created_at
gastos             — id, obra_id, telegram_id, descripcion, monto, categoria, created_at
contactos          — id, constructor_id, nombre, telefono, rubro, created_at
presupuesto_items  — id, obra_id, descripcion, cantidad, unidad, precio_unitario, created_at
```

---

## WORKFLOW N8N (estado actual — 7 nodos)

```
Webhook → HTTP Request (/mensaje)
                ↓
              IF (respuesta contains [GENERAR_PDF])
             /                        \
           TRUE                      FALSE
            ↓                          ↓
  HTTP Request1 (/presupuesto/pdf)    Merge
            ↓                          ↓
  Send Document (Telegram)      Send text message (Telegram)
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
2. **Voz (Groq)** — transcribir audios de Telegram (pendiente por costo API)
3. **Recordatorios** — "avisame mañana a las 8"
4. **Registrar medidas** — "la pared norte mide 8.40m"
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

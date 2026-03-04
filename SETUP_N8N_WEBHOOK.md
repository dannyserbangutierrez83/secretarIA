# ════════════════════════════════════════════════════════════════
# SETUP N8N: Webhook + Flujo para SecretarIA
# ════════════════════════════════════════════════════════════════

## PASO 1: Acceder a n8n

1. Abre: `http://localhost:5678`
2. Crea una cuenta (email: test@example.com, cualquier contraseña)
3. Haz click en **"New Workflow"**

---

## PASO 2: Crear Webhook (Receptor de WATI)

1. Busca el nodo **"Webhook"** en el panel izquierdo
2. Arrastra a la canvas
3. Configura:
   - **Method:** POST
   - **Path:** `/secretaria`
   - Dale a **"Save"**

Punto clave: El webhook URL será:
```
http://localhost:5678/webhook/secretaria
```

---

## PASO 3: Agregar nodo HTTP Request (para Railway API)

1. Busca **"HTTP Request"** en el panel izquierdo
2. Arrastra al canvas (conecta al Webhook)
3. Configura:

```
URL: https://web-production-a5da.up.railway.app/mensaje
Method: POST
Headers:
  - Content-Type: application/json

Body:
{
  "constructor_id": "{{ $json.body.constructor_id }}",
  "obra_nombre": "{{ $json.body.obra_nombre }}",
  "texto": "{{ $json.body.mensaje }}"
}
```

4. Click en **"Test"**

---

## PASO 4: Agregar nodo Response (devolver respuesta)

1. Busca **"Respond to Webhook"** en el panel izquierdo
2. Arrastra al canvas (conecta del HTTP Request)
3. Configura:

```
Body (Respuesta):
{
  "status": "ok",
  "respuesta": "{{ $json.respuesta }}",
  "obra_id": "{{ $json.obra_id }}"
}
```

---

## PASO 5: Guardar Workflow

1. Click arriba en **"Save"**
2. Dale un nombre: `SecretarIA - WATI Integration`
3. Click **"Active"** para activarlo (debe estar ON)

---

## PASO 6: Test del Flujo

Ejecuta en PowerShell:

```powershell
$headers = @{"Content-Type" = "application/json"}
$body = @{
    constructor_id = "test-001"
    obra_nombre = "Test"
    mensaje = "Necesito 50 bolsas de cemento"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5678/webhook/secretaria" `
  -Method POST `
  -Headers $headers `
  -Body $body | Select-Object -ExpandProperty Content
```

Debe retornar:
```json
{
  "status": "ok",
  "respuesta": "Listo, agregué...",
  "obra_id": 3
}
```

---

## PASO 7: Exportar Workflow

1. Click al menú (tres puntos) en n8n
2. **Download Workflow**
3. Guarda como: `n8n_secretaria_workflow.json`
4. Commitea a GitHub

---

## 🔗 FLUJO FINAL

```
WATI Webhook
    ↓
n8n (localhost:5678/webhook/secretaria)
    ↓
HTTP Request → Railway API (/mensaje)
    ↓
Claude responde
    ↓
Supabase guarda
    ↓
Response devuelve al webhook
    ↓
WATI envía al WhatsApp
```

---

## ❌ TROUBLESHOOTING

| Problema | Solución |
|----------|----------|
| "Cannot connect to localhost:5678" | Verificar: `docker ps` debe mostrar n8n running |
| Webhook no dispara | Verificar que esté **Activo** (verde) |
| "Railway API returns 500" | Ver logs: `docker logs n8n` |
| Error de headers | Asegurate que sea **exactly** `Content-Type: application/json` |

---

## 📝 NOTAS

- n8n guarda workflows localmente en volumen Docker
- Para próxima sesión, workflows se mantienen
- Para eliminar todo: `docker volume rm n8n_data && docker rm n8n`

---

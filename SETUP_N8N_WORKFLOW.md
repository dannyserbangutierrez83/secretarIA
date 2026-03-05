# ════════════════════════════════════════════════════════════════
# SETUP N8N WORKFLOW — SecretarIA
# Guía paso a paso para crear flujo webhook → Railway API
# ════════════════════════════════════════════════════════════════

## 1️⃣ INICIAR N8N EN DOCKER

```powershell
docker run -p 5678:5678 n8nio/n8n
```

Acceder a: http://localhost:5678

---

## 2️⃣ CREAR NUEVO WORKFLOW

**Nombre:** `SecretarIA WATI Integration`
**Descripción:** Webhook from WATI → Railway API → Claude → Supabase

---

## 3️⃣ AGREGAR WEBHOOK NODE

1. Click en `+` → Search `Webhook`
2. Configurar:
   - **HTTP Method:** POST
   - **Path:** `/secretaria-webhook`
   - **Authentication:** None (por ahora)
3. Test URL: `http://localhost:5678/webhook/secretaria-webhook`

**Entrada esperada:**
```json
{
  "constructor_id": "dario-obra-001",
  "obra_nombre": "Obra Principal",
  "texto": "Necesito 20 bolsas de cemento"
}
```

---

## 4️⃣ AGREGAR HTTP REQUEST NODE

1. Click en `+` después del Webhook → Search `HTTP Request`
2. Conectar: Webhook → HTTP Request
3. Configurar:

| Campo | Valor |
|-------|-------|
| **Method** | POST |
| **URL** | `https://web-production-a5da.up.railway.app/mensaje` |
| **Authentication** | None |
| **Send Headers** | ✓ |
| **Header Content-Type** | `application/json` |

**Body (JSON):**
```json
{
  "constructor_id": "{{ $json.constructor_id }}",
  "obra_nombre": "{{ $json.obra_nombre }}",
  "texto": "{{ $json.texto }}"
}
```

---

## 5️⃣ AGREGAR RESPONSE NODE

1. Click en `+` después de HTTP Request → Search `Respond to Webhook`
2. Conectar: HTTP Request → Respond to Webhook
3. Configurar:

| Campo | Valor |
|-------|-------|
| **Status Code** | 200 |
| **Response Body** | `{{ $json }}` |

---

## 6️⃣ WORKFLOW VISUAL

```
┌─────────────────────┐
│   WATI Webhook      │
│  (POST /secretaria) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│  HTTP Request to Railway    │
│  POST /mensaje              │
│  Body: { constructor_id,    │
│          obra_nombre,       │
│          texto }            │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────┐
│  Respond to Webhook │
│  Status: 200        │
│  Body: Response     │
└─────────────────────┘
```

---

## 7️⃣ ACTIVAR WORKFLOW

1. Click en **Save**
2. Click en toggle **Active** (arriba derecha)
3. Status debe mostrar 🟢 **Active**

---

## 8️⃣ TEST LOCAL

### Opción A: Con curl

```powershell
$body = @{
    constructor_id = "dario-obra-001"
    obra_nombre = "Obra Principal"
    texto = "Necesito 20 bolsas de cemento"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5678/webhook/secretaria-webhook" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

### Opción B: Con test_n8n_flow.py (ver archivo)

---

## 9️⃣ VALIDAR RESPUESTA

**Respuesta esperada:**
```json
{
  "respuesta": "He registrado tu solicitud: 20 bolsas de cemento...",
  "items_agregados": 2,
  "lista_actual": [...]
}
```

---

## 🔟 EXPORTAR WORKFLOW

1. Click en **Menu** (⋮)
2. Click **Export**
3. Guardar como `n8n_secretaria_workflow.json`
4. Commitar a GitHub

---

## 🆘 TROUBLESHOOTING

| Problema | Solución |
|----------|----------|
| Webhook URL no funciona | Verificar que n8n esté on http://localhost:5678 |
| Railway API retorna 404 | Verificar que el endpoint /mensaje existe |
| No recibe POST | Verificar que Webhook esté **Active** |
| CORS error | Agregar header `Access-Control-Allow-Origin: *` |

---

## 📝 NOTAS

- Por ahora sin autenticación (seguridad luego)
- WATI enviará JSON similar a este formato
- Railway API transforma → Claude llama con tools → Supabase guarda
- Respuesta vuelve a n8n → n8n podría enviar a WATI después

---

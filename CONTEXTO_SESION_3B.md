# CONTEXTO SESION 3B — SecretarIA
# Fecha: Marzo 5, 2026

## ESTADO ACTUAL

**Progreso:** 80% completado. Fases 1, 2, 3 completas. n8n corriendo en Docker.

### COMPLETADO HOY (Sesion 3A):
- WSL actualizado (`wsl --update`)
- Docker Desktop funcionando
- n8n corriendo en Docker: `docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n`
- n8n accesible en http://localhost:5678
- Workflow nuevo creado en n8n (el anterior archivado por nodo fantasma)

### EN PROGRESO AHORA:
Creando workflow nuevo desde cero en n8n.
Paso actual: Webhook node configurado (POST, path: secretaria-webhook), volviendo al canvas.

---

## ARQUITECTURA

```
WhatsApp -> WATI -> n8n (localhost:5678) -> Railway API -> Claude -> Supabase
```

**Railway API (produccion):**
- GET  https://web-production-a5da.up.railway.app/health  -> OK confirmado
- POST https://web-production-a5da.up.railway.app/mensaje -> OK confirmado via curl
- POST https://web-production-a5da.up.railway.app/lista

**Formato /mensaje:**
```json
{
  "constructor_id": "dario-obra-001",
  "obra_nombre": "Obra Principal",
  "texto": "Necesito 20 bolsas de cemento"
}
```

**GitHub:** https://github.com/dannyserbangutierrez83/secretarIA

---

## PROXIMOS PASOS EN N8N (workflow nuevo)

El workflow tiene que ser SOLO 2 nodos (sin Respond to Webhook — causa errores):

### Nodo 1: Webhook
- HTTP Method: POST
- Path: secretaria-webhook
- URL resultado: http://localhost:5678/webhook/secretaria-webhook

### Nodo 2: HTTP Request
- Method: POST
- URL: https://web-production-a5da.up.railway.app/mensaje
- Body Content Type: JSON
- Body (modo expression activado): `{{ JSON.stringify($json.body) }}`
  - IMPORTANTE: en n8n nuevo los datos del webhook llegan en $json.body
  - Si $json.body no funciona, probar $json directamente
  - La palabra "constructor" en campo nombre da error -> usar $json["constructor_id"]

### NO agregar nodo "Respond to Webhook" — causa error "Unused node"

### Test:
```powershell
$body = @{
    constructor_id = "dario-obra-001"
    obra_nombre = "Obra Principal"
    texto = "Necesito 20 bolsas de cemento y 5 kg de clavos"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5678/webhook/secretaria-webhook" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

---

## LECCION APRENDIDA HOY

- n8n bloquea la palabra "constructor" en expresiones (seguridad JS)
  - Usar $json["constructor_id"] en vez de $json.constructor_id
- "Respond to Webhook" node causa problemas si no esta correctamente conectado
  - Solucion: NO usarlo, n8n responde automaticamente con el ultimo nodo
- En n8n nuevo (v2.10.3), datos del webhook POST pueden estar en $json.body

---

## DOCKER COMMANDS

```bash
# Ver si n8n corre
docker ps

# Logs de n8n
docker logs n8n --tail 50

# Parar n8n
docker stop n8n

# Reiniciar n8n
docker start n8n
```

---

## STACK COMPLETO

- **Supabase:** Schema obras + items, CRUD funcionando
- **agente_obra.py:** Agente Python con Claude API (tool use)
- **api.py:** Flask API con /health /mensaje /lista
- **Railway:** Deploy automatico desde GitHub (branch main)
- **n8n:** Docker local v2.10.3, puerto 5678
- **WATI:** Pendiente (Sesion 4)

---

## CONTEXTO DE NEGOCIO

- Cliente: Dario (constructor uruguayo)
- Problema: Se olvida materiales en obra
- Solucion: WhatsApp + IA que nunca olvida
- Demo objetivo: 2 semanas

# SETUP: Voz con Groq Whisper en n8n
# SecretarIA — Sesión 6

## OBJETIVO

Detectar si el mensaje de Telegram es de voz → transcribir con Groq Whisper → enviar texto transcripto a la Railway API.

La API (`api.py`) NO necesita cambios. Solo se modifica el workflow de n8n.

---

## FLUJO COMPLETO CON VOZ

```
Telegram (voz o texto)
        ↓
  [Telegram Trigger]
        ↓
  [IF: ¿es voz?]
   ↙          ↘
 SÍ            NO
  ↓             ↓
[Get File]   [Set texto]
  ↓
[Download]
  ↓
[Groq Whisper]
  ↓
[Set texto]
   ↘          ↙
    [Merge textos]
         ↓
  [HTTP → Railway API]
         ↓
  [Telegram send]
```

---

## NODOS A AGREGAR (en orden)

### NODO 1: IF — ¿Es mensaje de voz?

- **Tipo:** IF
- **Condición:**
  - Campo: `{{ $json.message.voice }}`
  - Operación: `is not empty`
- **Nombre sugerido:** `¿Es voz?`

---

### NODO 2 (rama VOZ): HTTP Request — Obtener archivo de Telegram

Telegram no manda el audio directo, hay que pedir la URL de descarga.

- **Tipo:** HTTP Request
- **Method:** GET
- **URL:** `https://api.telegram.org/bot{{ $env.TELEGRAM_BOT_TOKEN }}/getFile`
- **Query Parameters:**
  - `file_id` → `{{ $json.message.voice.file_id }}`
- **Nombre sugerido:** `Telegram: Get File`

**Respuesta esperada:**
```json
{
  "result": {
    "file_path": "voice/file_123.ogg"
  }
}
```

---

### NODO 3 (rama VOZ): HTTP Request — Descargar audio

- **Tipo:** HTTP Request
- **Method:** GET
- **URL:** `https://api.telegram.org/file/bot{{ $env.TELEGRAM_BOT_TOKEN }}/{{ $json.result.file_path }}`
- **Response Format:** `File`  ← **importante**, no JSON
- **Nombre sugerido:** `Descargar audio`

---

### NODO 4 (rama VOZ): HTTP Request — Groq Whisper

- **Tipo:** HTTP Request
- **Method:** POST
- **URL:** `https://api.groq.com/openai/v1/audio/transcriptions`
- **Authentication:** None (manual en headers)
- **Headers:**
  - `Authorization` → `Bearer {GROQ_API_KEY}` ← **única cosa que necesita cuenta**
- **Body:** Form Data (multipart)
  - `file` → `{{ $binary.data }}` (el audio descargado)
  - `model` → `whisper-large-v3`
  - `language` → `es`
  - `response_format` → `json`
- **Nombre sugerido:** `Groq Whisper`

**Respuesta esperada:**
```json
{
  "text": "necesito veinte bolsas de cemento"
}
```

---

### NODO 5 (rama VOZ): Set — Extraer texto transcripto

- **Tipo:** Set
- **Campos:**
  - `texto_final` → `{{ $json.text }}`
- **Nombre sugerido:** `Set texto voz`

---

### NODO 6 (rama TEXTO): Set — Extraer texto del mensaje

- **Tipo:** Set
- **Campos:**
  - `texto_final` → `{{ $('Telegram Trigger').item.json.message.text }}`
- **Nombre sugerido:** `Set texto escrito`

---

### NODO 7: Merge — Unir ambas ramas

- **Tipo:** Merge
- **Mode:** `Append` o `Combine` (lo que llegue primero)
- **Nombre sugerido:** `Merge textos`

---

### NODO 8: HTTP Request — Railway API (REEMPLAZA el nodo actual)

Ajustar el nodo existente para usar `texto_final` en lugar de `message.text`:

- **Body:**
  - `texto` → `{{ $json.texto_final }}`
  - `constructor_id` → `{{ $('Telegram Trigger').item.json.message.chat.id }}`
  - `obra_nombre` → `Obra Principal`

---

## VARIABLE DE ENTORNO EN N8N (Railway)

Verificar que en el servicio n8n de Railway esté definida:

```
TELEGRAM_BOT_TOKEN=tu_token_aqui
```

Si no está, agregarla en: Railway → n8n service → Variables

---

## PASOS CUANDO TENGAS LA KEY DE GROQ

1. Ir a: https://console.groq.com → API Keys → Create API Key
2. Copiar la key
3. En n8n, en el nodo `Groq Whisper`:
   - Headers → Authorization → `Bearer {pegar_key_aquí}`
4. Activar workflow
5. Probar enviando un audio de voz al bot de Telegram

---

## NOTAS TÉCNICAS

- Telegram envía audios de voz en formato `.ogg` (opus codec)
- Groq Whisper acepta: mp3, mp4, mpeg, mpga, m4a, wav, webm, **ogg** ✓
- Límite de Groq: 25 MB por archivo (sobra para mensajes de voz)
- Costo estimado: ~$0.02 por hora de audio (Groq es muy barato)
- `whisper-large-v3` es el más preciso; también existe `whisper-large-v3-turbo` (más rápido, algo menos preciso)

---

## ALTERNATIVA: OpenAI Whisper (si Groq falla)

Si Groq tiene problemas, el mismo nodo funciona con OpenAI:
- URL: `https://api.openai.com/v1/audio/transcriptions`
- Model: `whisper-1`
- Costo: más caro (~$0.006/minuto vs casi gratis en Groq)

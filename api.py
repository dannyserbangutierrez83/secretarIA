"""
API Flask para SecretarIA
Expone agente_obra.py como servicio HTTP para integración con n8n/Telegram
"""
import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import anthropic
from supabase import create_client, Client

# ── Configuración ──────────────────────────────────────────────────────────────
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
anthropic_client = anthropic.Anthropic()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

MAX_OBRAS = 5

# ── Sistema prompt del agente ──────────────────────────────────────────────────
SYSTEM_PROMPT = """Sos SecretarIA, el asistente de obra de un constructor uruguayo.
Tu trabajo es ayudarlo a no olvidar nada: materiales, tareas, llamadas pendientes.

Hablás de forma directa y simple, como hablaría alguien en obra.
Usás las herramientas disponibles para guardar, mostrar, marcar y limpiar la lista.

Reglas:
- Si el constructor menciona algo que necesita comprar o hacer → usá guardar_item
- Si menciona cantidad (ej: "20 bolsas") → guardá con el campo cantidad
- Si pregunta qué tiene pendiente → usá ver_lista
- Si dice que compró TODO de algo → usá marcar_comprado con el ID correcto
- Si dice que compró UNA PARTE (ej: "compré 10 de las 20 bolsas") → usá actualizar_cantidad
- Si pregunta cuánto material necesita para una obra o trabajo → usá calcular_materiales
- Después de calcular_materiales, mostrá el resultado y preguntá si lo agregás a la lista. Si confirma, guardá cada material con guardar_item
- Si pide limpiar los comprados → usá limpiar_lista
- Confirmá siempre lo que hiciste en lenguaje simple
- No inventes IDs, primero mostrá la lista si no sabés los IDs
- Nunca menciones los IDs al usuario, son solo para uso interno tuyo
- Cuando listés items, mostralos sin el número de ID"""

# ── Herramientas ───────────────────────────────────────────────────────────────
TOOLS = [
    {
        "name": "guardar_item",
        "description": "Guarda un material o tarea pendiente en la lista de obra. Si el usuario menciona una cantidad, guardala en cantidad_total.",
        "input_schema": {
            "type": "object",
            "properties": {
                "item": {
                    "type": "string",
                    "description": "El material o tarea a guardar. Ej: 'bolsas de cemento'"
                },
                "cantidad": {
                    "type": "number",
                    "description": "Cantidad total necesaria. Ej: 20. Omitir si no se menciona cantidad."
                }
            },
            "required": ["item"]
        }
    },
    {
        "name": "ver_lista",
        "description": "Muestra todos los items pendientes de la lista de obra.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "marcar_comprado",
        "description": "Marca uno o varios items como completamente comprados.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ids": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Lista de IDs de los items a marcar como comprados."
                }
            },
            "required": ["ids"]
        }
    },
    {
        "name": "actualizar_cantidad",
        "description": "Registra que se compró una parte de un item con cantidad. Resta lo comprado del pendiente. Si queda 0 o menos, lo marca como comprado.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "ID del item a actualizar."
                },
                "cantidad_comprada": {
                    "type": "number",
                    "description": "Cantidad que se compró ahora."
                }
            },
            "required": ["id", "cantidad_comprada"]
        }
    },
    {
        "name": "calcular_materiales",
        "description": "Calcula los materiales necesarios para un trabajo de construcción según el tipo y las medidas. Devuelve una lista con cantidades estimadas.",
        "input_schema": {
            "type": "object",
            "properties": {
                "tipo_trabajo": {
                    "type": "string",
                    "description": "Tipo de trabajo. Ej: 'losa', 'pared de ladrillos', 'contrapiso', 'revoque', 'pintura interior'"
                },
                "medidas": {
                    "type": "string",
                    "description": "Medidas del trabajo. Ej: '40m2', '10m x 3m de alto', '6m x 4m x 0.15m de espesor'"
                },
                "aclaraciones": {
                    "type": "string",
                    "description": "Detalles adicionales opcionales. Ej: 'es hormigón armado', 'ladrillo hueco 18cm', 'dos manos de pintura'"
                }
            },
            "required": ["tipo_trabajo", "medidas"]
        }
    },
    {
        "name": "limpiar_lista",
        "description": "Elimina todos los items ya comprados/completados de la lista.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

# ── Funciones de herramientas (Claude) ────────────────────────────────────────
def guardar_item(obra_id: int, item: str, cantidad: float = None) -> str:
    try:
        datos = {
            "obra_id": obra_id,
            "item": item,
            "comprado": False,
            "fecha_anotacion": datetime.now().isoformat()
        }
        if cantidad is not None:
            datos["cantidad_total"] = cantidad
            datos["cantidad_pendiente"] = cantidad

        resp = supabase.table("items").insert(datos).execute()
        new_id = resp.data[0]["id"]
        if cantidad is not None:
            return f"✅ Guardado: '{item}' — cantidad: {cantidad} (ID: {new_id})"
        return f"✅ Guardado: '{item}' (ID: {new_id})"
    except Exception as e:
        logger.error(f"Error guardando item: {e}")
        return f"❌ Error guardando: {str(e)}"

def ver_lista(obra_id: int) -> str:
    try:
        resp = supabase.table("items").select("id, item, comprado, fecha_anotacion, cantidad_total, cantidad_pendiente").eq("obra_id", obra_id).execute()

        if not resp.data:
            return "La lista está vacía."

        pendientes = [i for i in resp.data if not i["comprado"]]
        comprados  = [i for i in resp.data if i["comprado"]]

        resp_text = ""
        if pendientes:
            resp_text += "📋 *PENDIENTES:*\n"
            for item in pendientes:
                fecha = item["fecha_anotacion"][:10] if item["fecha_anotacion"] else "?"
                if item.get("cantidad_total") is not None:
                    cant = f" — {item['cantidad_pendiente']}/{item['cantidad_total']} pendientes"
                else:
                    cant = ""
                resp_text += f"  [{item['id']}] {item['item']}{cant}  _(anotado {fecha})_\n"

        if comprados:
            resp_text += "\n✅ *YA COMPRADO:*\n"
            for item in comprados:
                resp_text += f"  [{item['id']}] ~~{item['item']}~~\n"

        return resp_text.strip()
    except Exception as e:
        logger.error(f"Error leyendo lista: {e}")
        return f"❌ Error leyendo lista: {str(e)}"

def actualizar_cantidad(obra_id: int, id: int, cantidad_comprada: float) -> str:
    try:
        resp = supabase.table("items").select("id, item, cantidad_total, cantidad_pendiente").eq("id", id).eq("obra_id", obra_id).execute()
        if not resp.data:
            return f"⚠️ No encontré el item con ID {id}."

        row = resp.data[0]
        if row["cantidad_total"] is None:
            return f"⚠️ '{row['item']}' no tiene cantidad definida. Usá marcar_comprado si ya lo compraste todo."

        nueva_pendiente = (row["cantidad_pendiente"] or row["cantidad_total"]) - cantidad_comprada

        if nueva_pendiente <= 0:
            supabase.table("items").update({
                "cantidad_pendiente": 0,
                "comprado": True,
                "fecha_compra": datetime.now().isoformat()
            }).eq("id", id).execute()
            return f"✅ '{row['item']}' completado. Compraste todo."
        else:
            supabase.table("items").update({"cantidad_pendiente": nueva_pendiente}).eq("id", id).execute()
            return f"✅ '{row['item']}': compraste {cantidad_comprada}, quedan {nueva_pendiente} pendientes."
    except Exception as e:
        logger.error(f"Error actualizando cantidad: {e}")
        return f"❌ Error: {str(e)}"

def marcar_comprado(obra_id: int, ids: list) -> str:
    try:
        # Un SELECT para todos los IDs pedidos
        resp = supabase.table("items").select("id, item").in_("id", ids).eq("obra_id", obra_id).execute()
        encontrados = {row["id"]: row["item"] for row in resp.data}
        ids_validos = list(encontrados.keys())
        no_encontrados = [i for i in ids if i not in encontrados]

        # Un UPDATE para todos los válidos
        if ids_validos:
            supabase.table("items").update({
                "comprado": True,
                "fecha_compra": datetime.now().isoformat()
            }).in_("id", ids_validos).execute()

        resp_text = ""
        if ids_validos:
            resp_text += "✅ Marcado como comprado: " + ", ".join(f"'{encontrados[i]}'" for i in ids_validos)
        if no_encontrados:
            resp_text += f"\n⚠️ No encontré los IDs: {no_encontrados}"

        return resp_text.strip() if resp_text else "No se actualizó nada."
    except Exception as e:
        logger.error(f"Error marcando: {e}")
        return f"❌ Error marcando: {str(e)}"

def limpiar_lista(obra_id: int) -> str:
    try:
        # Un solo DELETE — Supabase retorna las filas eliminadas
        resp = supabase.table("items").delete().eq("obra_id", obra_id).eq("comprado", True).execute()
        antes = len(resp.data)

        if antes == 0:
            return "No había items comprados para limpiar."

        return f"🗑️ Se eliminaron {antes} item(s) ya comprados. Lista actualizada."
    except Exception as e:
        logger.error(f"Error limpiando: {e}")
        return f"❌ Error limpiando: {str(e)}"

def calcular_materiales(tipo_trabajo: str, medidas: str, aclaraciones: str = "") -> str:
    # Claude ya tiene el conocimiento — esta función solo devuelve los parámetros
    # para que Claude genere la respuesta con su propio razonamiento
    detalle = f"Tipo de trabajo: {tipo_trabajo}\nMedidas: {medidas}"
    if aclaraciones:
        detalle += f"\nAclaraciones: {aclaraciones}"
    detalle += "\n\nCalculá los materiales necesarios con cantidades estimadas, incluyendo un 10% de desperdicio. Listá cada material con su cantidad y unidad."
    return detalle

def ejecutar_herramienta(nombre: str, inputs: dict, obra_id: int) -> str:
    if nombre == "guardar_item":
        return guardar_item(obra_id, inputs["item"], inputs.get("cantidad"))
    elif nombre == "ver_lista":
        return ver_lista(obra_id)
    elif nombre == "marcar_comprado":
        return marcar_comprado(obra_id, inputs["ids"])
    elif nombre == "actualizar_cantidad":
        return actualizar_cantidad(obra_id, inputs["id"], inputs["cantidad_comprada"])
    elif nombre == "calcular_materiales":
        return calcular_materiales(inputs["tipo_trabajo"], inputs["medidas"], inputs.get("aclaraciones", ""))
    elif nombre == "limpiar_lista":
        return limpiar_lista(obra_id)
    else:
        return f"Herramienta desconocida: {nombre}"

# ── Usuarios y obras ───────────────────────────────────────────────────────────
def obtener_usuario(telegram_id: str) -> tuple[bool, int | None]:
    """
    Una sola query: retorna (activo, obra_activa_id).
    Usado en el endpoint /mensaje para evitar dos queries a la tabla usuarios.
    """
    try:
        resp = supabase.table("usuarios").select("activo, obra_activa_id").eq("telegram_id", telegram_id).execute()
        if not resp.data:
            return False, None
        row = resp.data[0]
        return bool(row["activo"]), row["obra_activa_id"]
    except Exception as e:
        logger.error(f"Error obteniendo usuario: {e}")
        return False, None

def obtener_obra_activa(telegram_id: str) -> int | None:
    """Retorna el obra_id activo del usuario."""
    _, obra_activa_id = obtener_usuario(telegram_id)
    return obra_activa_id

def _obras_del_usuario(telegram_id: str) -> list:
    """Helper compartido: retorna lista de obras del constructor ordenadas por id."""
    resp = supabase.table("obras").select("id, nombre").eq("constructor_id", telegram_id).order("id").execute()
    return resp.data or []

def listar_obras(telegram_id: str) -> str:
    try:
        obras = _obras_del_usuario(telegram_id)
        _, obra_activa_id = obtener_usuario(telegram_id)

        if not obras:
            return "No tenés obras todavía. Creá una con:\n/nueva Nombre de la obra"

        lineas = []
        for i, obra in enumerate(obras, 1):
            activa = " ← activa" if obra["id"] == obra_activa_id else ""
            lineas.append(f"{i}. {obra['nombre']}{activa}")

        lineas.append(f"\n{len(obras)}/{MAX_OBRAS} obras. Para cambiar: /cambiar 2")
        return "\n".join(lineas)
    except Exception as e:
        logger.error(f"Error listando obras: {e}")
        return f"❌ Error: {str(e)}"

def crear_obra(telegram_id: str, nombre: str) -> str:
    try:
        obras_existentes = _obras_del_usuario(telegram_id)

        if len(obras_existentes) >= MAX_OBRAS:
            return f"⚠️ Ya tenés {MAX_OBRAS} obras (el máximo). Eliminá una antes de crear otra."

        nueva = supabase.table("obras").insert({
            "nombre": nombre,
            "constructor_id": telegram_id,
            "creada_en": datetime.now().isoformat()
        }).execute()

        nueva_id = nueva.data[0]["id"]
        supabase.table("usuarios").update({"obra_activa_id": nueva_id}).eq("telegram_id", telegram_id).execute()

        total = len(obras_existentes) + 1
        return f"✅ Obra '{nombre}' creada y activada. Tenés {total}/{MAX_OBRAS} obras."
    except Exception as e:
        logger.error(f"Error creando obra: {e}")
        return f"❌ Error: {str(e)}"

def cambiar_obra(telegram_id: str, numero: str) -> str:
    try:
        if not numero.isdigit():
            return "⚠️ Usá un número. Ej: /cambiar 2"

        obras = _obras_del_usuario(telegram_id)

        if not obras:
            return "No tenés obras. Creá una con /nueva Nombre"

        idx = int(numero) - 1
        if idx < 0 or idx >= len(obras):
            return f"⚠️ Número inválido. Tenés {len(obras)} obras."

        obra = obras[idx]
        supabase.table("usuarios").update({"obra_activa_id": obra["id"]}).eq("telegram_id", telegram_id).execute()

        return f"✅ Cambiaste a '{obra['nombre']}'"
    except Exception as e:
        logger.error(f"Error cambiando obra: {e}")
        return f"❌ Error: {str(e)}"

def manejar_comando(telegram_id: str, texto: str) -> str | None:
    """
    Detecta y ejecuta comandos especiales.
    Retorna la respuesta si era un comando, None si no lo era.
    """
    texto = texto.strip()

    if texto == "/obras":
        return listar_obras(telegram_id)

    if texto.startswith("/nueva "):
        nombre = texto.removeprefix("/nueva ").strip()
        if not nombre:
            return "⚠️ Escribí el nombre de la obra. Ej: /nueva Casa Playa"
        return crear_obra(telegram_id, nombre)

    if texto.startswith("/cambiar "):
        numero = texto.removeprefix("/cambiar ").strip()
        return cambiar_obra(telegram_id, numero)

    if texto == "/ayuda":
        return (
            "📋 *Comandos disponibles:*\n"
            "/obras — ver tus obras\n"
            "/nueva Nombre — crear obra nueva\n"
            "/cambiar 2 — cambiar a la obra número 2\n"
            "/ayuda — este mensaje\n\n"
            "Para todo lo demás, escribí normalmente y te ayudo."
        )

    return None

# ── Historial de conversación ──────────────────────────────────────────────────
MAX_HISTORIAL = 10  # últimos N mensajes (user + assistant)

def cargar_historial(telegram_id: str, obra_id: int) -> list:
    try:
        resp = supabase.table("mensajes") \
            .select("role, content") \
            .eq("telegram_id", telegram_id) \
            .eq("obra_id", obra_id) \
            .order("created_at", desc=True) \
            .limit(MAX_HISTORIAL) \
            .execute()
        mensajes = list(reversed(resp.data or []))
        return [{"role": m["role"], "content": m["content"]} for m in mensajes]
    except Exception as e:
        logger.error(f"Error cargando historial: {e}")
        return []

def guardar_en_historial(telegram_id: str, obra_id: int, role: str, content: str):
    try:
        supabase.table("mensajes").insert({
            "telegram_id": telegram_id,
            "obra_id": obra_id,
            "role": role,
            "content": content,
            "created_at": datetime.now().isoformat()
        }).execute()
    except Exception as e:
        logger.error(f"Error guardando historial: {e}")

# ── Procesar mensajes con Claude ───────────────────────────────────────────────
def procesar_mensaje(mensaje_usuario: str, obra_id: int, telegram_id: str) -> str:
    historial_previo = cargar_historial(telegram_id, obra_id)
    historial = historial_previo + [{"role": "user", "content": mensaje_usuario}]

    while True:
        try:
            response = anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=historial
            )

            historial.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "tool_use":
                resultados = []
                for bloque in response.content:
                    if bloque.type == "tool_use":
                        resultado = ejecutar_herramienta(bloque.name, bloque.input, obra_id)
                        resultados.append({
                            "type": "tool_result",
                            "tool_use_id": bloque.id,
                            "content": resultado
                        })
                historial.append({"role": "user", "content": resultados})
                continue

            for bloque in response.content:
                if hasattr(bloque, "text"):
                    respuesta = bloque.text
                    guardar_en_historial(telegram_id, obra_id, "user", mensaje_usuario)
                    guardar_en_historial(telegram_id, obra_id, "assistant", respuesta)
                    return respuesta

            return "(sin respuesta)"

        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            return f"❌ Error: {str(e)}"

# ── Endpoints HTTP ─────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "SecretarIA API",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route("/mensaje", methods=["POST"])
def mensaje():
    """
    Procesa un mensaje de usuario.
    Espera JSON: { "texto": "...", "constructor_id": "123456789" }
    Retorna JSON: { "respuesta": "..." }
    """
    try:
        data = request.get_json()

        if not data or "texto" not in data:
            return jsonify({"error": "Falta campo 'texto'"}), 400

        texto = data.get("texto", "").strip()
        constructor_id = str(data.get("constructor_id", "")).strip()

        if not texto:
            return jsonify({"error": "El texto no puede estar vacío"}), 400
        if not constructor_id:
            return jsonify({"error": "Falta campo 'constructor_id'"}), 400

        # Una sola query a usuarios: auth + obra_activa
        activo, obra_id = obtener_usuario(constructor_id)

        if not activo:
            return jsonify({
                "respuesta": "Hola! Este servicio es privado. Contactá a @secretaria_ia para acceder. 🔒"
            }), 200

        # Detectar comandos especiales
        respuesta_comando = manejar_comando(constructor_id, texto)
        if respuesta_comando is not None:
            return jsonify({"respuesta": respuesta_comando}), 200

        # Mensaje normal → Claude
        if obra_id is None:
            return jsonify({
                "respuesta": "No tenés ninguna obra activa. Creá una con:\n/nueva Nombre de la obra"
            }), 200

        respuesta = procesar_mensaje(texto, obra_id, constructor_id)
        logger.info(f"Constructor {constructor_id} → OK")

        return jsonify({"respuesta": respuesta}), 200

    except Exception as e:
        logger.error(f"Error en /mensaje: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/lista", methods=["POST"])
def lista():
    """Obtiene la lista de items de la obra activa (sin IA)."""
    try:
        data = request.get_json()
        constructor_id = str(data.get("constructor_id", "")).strip()

        if not constructor_id:
            return jsonify({"error": "Falta 'constructor_id'"}), 400

        obra_id = obtener_obra_activa(constructor_id)
        if obra_id is None:
            return jsonify({"lista_texto": "No tenés obra activa.", "items": []}), 200

        # Una sola query: usamos los datos para texto formateado y JSON
        resp = supabase.table("items").select("id, item, comprado, fecha_anotacion").eq("obra_id", obra_id).execute()
        items = resp.data or []

        if not items:
            lista_texto = "La lista está vacía."
        else:
            pendientes = [i for i in items if not i["comprado"]]
            comprados  = [i for i in items if i["comprado"]]
            lineas = []
            if pendientes:
                lineas.append("📋 *PENDIENTES:*")
                for item in pendientes:
                    fecha = item["fecha_anotacion"][:10] if item["fecha_anotacion"] else "?"
                    lineas.append(f"  [{item['id']}] {item['item']}  _(anotado {fecha})_")
            if comprados:
                lineas.append("\n✅ *YA COMPRADO:*")
                for item in comprados:
                    lineas.append(f"  [{item['id']}] ~~{item['item']}~~")
            lista_texto = "\n".join(lineas)

        return jsonify({
            "obra_id": obra_id,
            "lista_texto": lista_texto,
            "items": items
        }), 200

    except Exception as e:
        logger.error(f"Error en /lista: {e}")
        return jsonify({"error": str(e)}), 500

# ── Error handlers ─────────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint no encontrado"}), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Error interno: {e}")
    return jsonify({"error": "Error interno del servidor"}), 500

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV", "production") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)

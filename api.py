"""
API Flask para SecretarIA
Expone agente_obra.py como servicio HTTP para integración con n8n/WATI
"""
import os
import json
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

# Clientes
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
anthropic_client = anthropic.Anthropic()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# ── Sistema prompt del agente ──────────────────────────────────────────────────
SYSTEM_PROMPT = """Sos SecretarIA, el asistente de obra de un constructor uruguayo.
Tu trabajo es ayudarlo a no olvidar nada: materiales, tareas, llamadas pendientes.

Hablás de forma directa y simple, como hablaría alguien en obra.
Usás las herramientas disponibles para guardar, mostrar, marcar y limpiar la lista.

Reglas:
- Si el constructor menciona algo que necesita comprar o hacer → usá guardar_item
- Si pregunta qué tiene pendiente → usá ver_lista  
- Si dice que ya compró algo → usá marcar_comprado con el ID correcto
- Si pide limpiar los comprados → usá limpiar_lista
- Confirmá siempre lo que hiciste en lenguaje simple
- No inventes IDs, primero mostrá la lista si no sabés los IDs"""

# ── Herramientas ───────────────────────────────────────────────────────────────
TOOLS = [
    {
        "name": "guardar_item",
        "description": "Guarda un material o tarea pendiente en la lista de obra.",
        "input_schema": {
            "type": "object",
            "properties": {
                "item": {
                    "type": "string",
                    "description": "El material o tarea a guardar. Ej: '20 bolsas de cemento'"
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
        "description": "Marca uno o varios items como comprados o completados.",
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
        "name": "limpiar_lista",
        "description": "Elimina todos los items ya comprados/completados de la lista.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

# ── Funciones de herramientas ──────────────────────────────────────────────────
def guardar_item(obra_id: int, item: str) -> str:
    """Guarda un item en Supabase."""
    try:
        resp = supabase.table("items").insert({
            "obra_id": obra_id,
            "item": item,
            "comprado": False,
            "fecha_anotacion": datetime.now().isoformat()
        }).execute()
        new_id = resp.data[0]["id"]
        return f"✅ Guardado: '{item}' (ID: {new_id})"
    except Exception as e:
        logger.error(f"Error guardando item: {e}")
        return f"❌ Error guardando: {str(e)}"

def ver_lista(obra_id: int) -> str:
    """Muestra pendientes y comprados desde Supabase."""
    try:
        resp = supabase.table("items").select("id, item, comprado, fecha_anotacion").eq("obra_id", obra_id).execute()
        
        if not resp.data:
            return "La lista está vacía."
        
        pendientes = [i for i in resp.data if not i["comprado"]]
        comprados = [i for i in resp.data if i["comprado"]]
        
        resp_text = ""
        if pendientes:
            resp_text += "📋 *PENDIENTES:*\n"
            for item in pendientes:
                fecha = item["fecha_anotacion"][:10] if item["fecha_anotacion"] else "?"
                resp_text += f"  [{item['id']}] {item['item']}  _(anotado {fecha})_\n"
        
        if comprados:
            resp_text += "\n✅ *YA COMPRADO:*\n"
            for item in comprados:
                resp_text += f"  [{item['id']}] ~~{item['item']}~~\n"
        
        return resp_text.strip()
    except Exception as e:
        logger.error(f"Error leyendo lista: {e}")
        return f"❌ Error leyendo lista: {str(e)}"

def marcar_comprado(obra_id: int, ids: list) -> str:
    """Marca items como comprados en Supabase."""
    try:
        marcados = []
        no_encontrados = []
        
        for id_buscado in ids:
            resp = supabase.table("items").select("item").eq("id", id_buscado).eq("obra_id", obra_id).execute()
            if resp.data:
                supabase.table("items").update({
                    "comprado": True,
                    "fecha_compra": datetime.now().isoformat()
                }).eq("id", id_buscado).execute()
                marcados.append(resp.data[0]["item"])
            else:
                no_encontrados.append(id_buscado)
        
        resp_text = ""
        if marcados:
            resp_text += "✅ Marcado como comprado: " + ", ".join(f"'{m}'" for m in marcados)
        if no_encontrados:
            resp_text += f"\n⚠️ No encontré los IDs: {no_encontrados}"
        
        return resp_text.strip() if resp_text else "No se actualizó nada."
    except Exception as e:
        logger.error(f"Error marcando: {e}")
        return f"❌ Error marcando: {str(e)}"

def limpiar_lista(obra_id: int) -> str:
    """Elimina items comprados de Supabase."""
    try:
        resp = supabase.table("items").select("id").eq("obra_id", obra_id).eq("comprado", True).execute()
        antes = len(resp.data)
        
        if antes == 0:
            return "No había items comprados para limpiar."
        
        for item in resp.data:
            supabase.table("items").delete().eq("id", item["id"]).execute()
        
        return f"🗑️ Se eliminaron {antes} item(s) ya comprados. Lista actualizada."
    except Exception as e:
        logger.error(f"Error limpiando: {e}")
        return f"❌ Error limpiando: {str(e)}"

def ejecutar_herramienta(nombre: str, inputs: dict, obra_id: int) -> str:
    if nombre == "guardar_item":
        return guardar_item(obra_id, inputs["item"])
    elif nombre == "ver_lista":
        return ver_lista(obra_id)
    elif nombre == "marcar_comprado":
        return marcar_comprado(obra_id, inputs["ids"])
    elif nombre == "limpiar_lista":
        return limpiar_lista(obra_id)
    else:
        return f"Herramienta desconocida: {nombre}"

def obtener_o_crear_obra(constructor_id: str, obra_nombre: str) -> int:
    """Obtiene la obra activa del constructor o crea una nueva."""
    try:
        resp = supabase.table("obras").select("id").eq("constructor_id", constructor_id).eq("activa", True).limit(1).execute()
        if resp.data:
            return resp.data[0]["id"]
        
        resp = supabase.table("obras").insert({
            "nombre": obra_nombre,
            "constructor_id": constructor_id,
            "activa": True
        }).execute()
        return resp.data[0]["id"]
    except Exception as e:
        logger.error(f"Error obteniendo/creando obra: {e}")
        raise

# ── Procesar mensajes con Claude ───────────────────────────────────────────────
def procesar_mensaje(mensaje_usuario: str, obra_id: int, historial: list = None) -> tuple[str, list]:
    """
    Procesa un mensaje con Claude usando tool use.
    Retorna (respuesta_final, historial_actualizado)
    """
    if historial is None:
        historial = []
    
    historial.append({"role": "user", "content": mensaje_usuario})
    
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
            
            # Si Claude quiere usar herramientas
            if response.stop_reason == "tool_use":
                resultados_herramientas = []
                for bloque in response.content:
                    if bloque.type == "tool_use":
                        resultado = ejecutar_herramienta(bloque.name, bloque.input, obra_id)
                        resultados_herramientas.append({
                            "type": "tool_result",
                            "tool_use_id": bloque.id,
                            "content": resultado
                        })
                
                historial.append({"role": "user", "content": resultados_herramientas})
                continue
            
            # Respuesta final
            for bloque in response.content:
                if hasattr(bloque, "text"):
                    return bloque.text, historial
            
            return "(sin respuesta)", historial
        
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            return f"❌ Error: {str(e)}", historial

# ── Endpoints HTTP ─────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint para Railway/Docker"""
    return jsonify({
        "status": "ok",
        "service": "SecretarIA API",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route("/mensaje", methods=["POST"])
def mensaje():
    """
    Procesa un mensaje de usuario.
    Espera JSON:
    {
        "texto": "necesito 20 bolsas de cemento",
        "constructor_id": "dario-obra-001",
        "obra_nombre": "Obra Principal"
    }
    Retorna JSON:
    {
        "respuesta": "✅ Guardado: '20 bolsas de cemento' (ID: 123)",
        "obra_id": 123
    }
    """
    try:
        data = request.get_json()
        
        # Validar inputs
        if not data or "texto" not in data:
            return jsonify({"error": "Falta campo 'texto'"}), 400
        
        texto = data.get("texto", "").strip()
        constructor_id = data.get("constructor_id", "usuario-default")
        obra_nombre = data.get("obra_nombre", "Obra Predeterminada")
        
        if not texto:
            return jsonify({"error": "El texto no puede estar vacío"}), 400
        
        # Obtener o crear obra
        obra_id = obtener_o_crear_obra(constructor_id, obra_nombre)
        
        # Procesar mensaje con Claude (sin guardar historial en la respuesta)
        respuesta, _ = procesar_mensaje(texto, obra_id, None)
        
        logger.info(f"Constructor {constructor_id} → Respuesta procesada")
        
        return jsonify({
            "respuesta": respuesta,
            "obra_id": obra_id
        }), 200
    
    except Exception as e:
        logger.error(f"Error en /mensaje: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/lista", methods=["POST"])
def lista():
    """Obtiene la lista de items de una obra (sin procesar con IA)."""
    try:
        data = request.get_json()
        constructor_id = data.get("constructor_id", "usuario-default")
        obra_nombre = data.get("obra_nombre", "Obra Predeterminada")
        
        obra_id = obtener_o_crear_obra(constructor_id, obra_nombre)
        lista_texto = ver_lista(obra_id)
        
        # Parsear la lista para retornar JSON
        resp = supabase.table("items").select("*").eq("obra_id", obra_id).execute()
        items = resp.data if resp.data else []
        
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

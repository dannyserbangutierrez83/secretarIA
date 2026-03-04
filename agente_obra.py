print("iniciando...")
import anthropic
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# ── Cargar variables de entorno ────────────────────────────────────────────────
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
CONSTRUCTOR_ID = os.getenv("CONSTRUCTOR_ID", "test-constructor")
OBRA_NOMBRE = os.getenv("OBRA_NOMBRE", "Obra de Prueba")

# ── Cliente Supabase ───────────────────────────────────────────────────────────
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── Inicializar obra (obtener o crear) ─────────────────────────────────────────
def init_obra():
    """Obtiene la obra activa del constructor, o crea una nueva."""
    try:
        # Buscar obra activa
        resp = supabase.table("obras").select("*").eq("constructor_id", CONSTRUCTOR_ID).eq("activa", True).limit(1).execute()
        if resp.data:
            return resp.data[0]["id"]
        
        # Si no existe, crear nueva
        resp = supabase.table("obras").insert({
            "nombre": OBRA_NOMBRE,
            "constructor_id": CONSTRUCTOR_ID,
            "activa": True
        }).execute()
        return resp.data[0]["id"]
    except Exception as e:
        print(f"Error inicializando obra: {e}")
        raise

OBRA_ID = init_obra()
print(f"✅ Obra conectada (ID: {OBRA_ID})")

# ── Definición de herramientas ─────────────────────────────────────────────────
tools = [
    {
        "name": "guardar_item",
        "description": "Guarda un material o tarea pendiente en la lista de obra. Úsala cuando el constructor mencione algo que necesita comprar, buscar o hacer.",
        "input_schema": {
            "type": "object",
            "properties": {
                "item": {
                    "type": "string",
                    "description": "El material o tarea a guardar. Ej: '20 bolsas de cemento', 'llamar al electricista', '3 caños de 4 pulgadas'"
                }
            },
            "required": ["item"]
        }
    },
    {
        "name": "ver_lista",
        "description": "Muestra todos los items pendientes de la lista de obra. Úsala cuando el constructor quiera saber qué tiene pendiente.",
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
                    "description": "Lista de IDs de los items a marcar como comprados. Los IDs se ven al usar ver_lista."
                }
            },
            "required": ["ids"]
        }
    },
    {
        "name": "limpiar_lista",
        "description": "Elimina todos los items ya comprados/completados de la lista. Úsala para mantener la lista limpia.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

# ── Lógica de cada herramienta ─────────────────────────────────────────────────
def guardar_item(item: str) -> str:
    """Guarda un item en Supabase."""
    try:
        resp = supabase.table("items").insert({
            "obra_id": OBRA_ID,
            "item": item,
            "comprado": False,
            "fecha_anotacion": datetime.now().isoformat()
        }).execute()
        new_id = resp.data[0]["id"]
        return f"✅ Guardado: '{item}' (ID: {new_id})"
    except Exception as e:
        return f"❌ Error guardando: {e}"

def ver_lista() -> str:
    """Muestra pendientes y comprados desde Supabase."""
    try:
        resp = supabase.table("items").select("id, item, comprado, fecha_anotacion").eq("obra_id", OBRA_ID).execute()
        
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
        return f"❌ Error leyendo lista: {e}"

def marcar_comprado(ids: list) -> str:
    """Marca items como comprados en Supabase."""
    try:
        marcados = []
        no_encontrados = []
        
        for id_buscado in ids:
            # Verificar que existe
            resp = supabase.table("items").select("item").eq("id", id_buscado).eq("obra_id", OBRA_ID).execute()
            if resp.data:
                # Actualizar a comprado
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
        return f"❌ Error marcando: {e}"

def limpiar_lista() -> str:
    """Elimina items comprados de Supabase."""
    try:
        # Contar los que vamos a eliminar
        resp = supabase.table("items").select("id").eq("obra_id", OBRA_ID).eq("comprado", True).execute()
        antes = len(resp.data)
        
        if antes == 0:
            return "No había items comprados para limpiar."
        
        # Eliminar todos los comprados
        for item in resp.data:
            supabase.table("items").delete().eq("id", item["id"]).execute()
        
        return f"🗑️ Se eliminaron {antes} item(s) ya comprados. Lista actualizada."
    except Exception as e:
        return f"❌ Error limpiando: {e}"

# ── Despacho de herramientas ───────────────────────────────────────────────────
def ejecutar_herramienta(nombre: str, inputs: dict) -> str:
    if nombre == "guardar_item":
        return guardar_item(inputs["item"])
    elif nombre == "ver_lista":
        return ver_lista()
    elif nombre == "marcar_comprado":
        return marcar_comprado(inputs["ids"])
    elif nombre == "limpiar_lista":
        return limpiar_lista()
    else:
        return f"Herramienta desconocida: {nombre}"

# ── Cliente Anthropic ──────────────────────────────────────────────────────────
client = anthropic.Anthropic()

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

historial = []

# ── Loop principal ─────────────────────────────────────────────────────────────
def procesar_mensaje(mensaje_usuario: str) -> str:
    historial.append({"role": "user", "content": mensaje_usuario})

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=historial
        )

        # Agregar respuesta al historial
        historial.append({"role": "assistant", "content": response.content})

        # Si Claude quiere usar herramientas
        if response.stop_reason == "tool_use":
            resultados_herramientas = []
            for bloque in response.content:
                if bloque.type == "tool_use":
                    resultado = ejecutar_herramienta(bloque.name, bloque.input)
                    resultados_herramientas.append({
                        "type": "tool_result",
                        "tool_use_id": bloque.id,
                        "content": resultado
                    })

            historial.append({"role": "user", "content": resultados_herramientas})
            # Volver a llamar para que Claude formule la respuesta final
            continue

        # Respuesta final en texto
        for bloque in response.content:
            if hasattr(bloque, "text"):
                return bloque.text

        return "(sin respuesta)"


def main():
    print("=" * 55)
    print("  SecretarIA — Memoria de Obra  ")
    print("  Escribí lo que necesitás recordar.")
    print("  Escribí 'salir' para terminar.")
    print("=" * 55)
    print()

    while True:
        try:
            entrada = input("Vos: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego.")
            break

        if not entrada:
            continue
        if entrada.lower() in ("salir", "exit", "chau"):
            print("SecretarIA: Hasta luego. Que salga bien la obra.")
            break

        respuesta = procesar_mensaje(entrada)
        print(f"\nSecretarIA: {respuesta}\n")


if __name__ == "__main__":
    main()
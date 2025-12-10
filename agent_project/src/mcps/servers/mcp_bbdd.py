import datetime
import sys

from pymongo import MongoClient, errors

from src.mcps.utils.log_mcp import log_mcp

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "gestion_clientes"
COLLECTION_NAME = "customers"

def init_db():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        # creamos índice único para probar el error desde el agente.
        collection.create_index("dni", unique=True)
        sys.stderr.write(f"BBDD MongoDB ('{DB_NAME}') inicializada.\n")
        client.close()
    except Exception:
        raise Exception("Error al iniciar la BBDD MongoDB")

@log_mcp
def guardar_cliente_db(dni: str, nombre_completo: str, email: str, direccion: str) -> str:
    """
    Registra oficialmente al cliente en MongoDB.
    ARGS:
    - dni: Identificador único.
    - nombre_completo: Nombre y apellidos.
    - email: Correo corporativo.
    - direccion: Dirección fiscal.
    """
    sys.stderr.write("==== guardar_cliente_db ====")
    client = None
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        client_doc = {
            "dni": dni,
            "nombre": nombre_completo,
            "email": email,
            "direccion": direccion,
            "status": "activo",
            "fecha_alta": datetime.datetime.now().isoformat()
        }
        collection.insert_one(client_doc)
        return f"Success: Client {nombre_completo} guardado en MongoDB."

    except errors.DuplicateKeyError:
        return f"Error: Ya existe un client con el DNI {dni}."
    except errors.ServerSelectionTimeoutError:
        return "Error crítico: No se puede conectar con MongoDB."
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if client: client.close()


def baja_cliente_db(dni: str, motivo: str) -> str:
    """
    Da de baja a un client. El cliente será actualizado en la base de datos MongoDB con estado "baja"
    y con el motivo de la baja registrado en la base de datos junto con la fecha de la baja.

    ARGS:
      - dni: El DNI exacto.
      - motivo: texto que indica el motivo de la baja.
    """
    client = None
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        resultado = collection.update_one(
            {
                "dni": dni,
                "status": "activo"
            },
            {
                "$set": {
                    "status": "baja",
                    "motivo_baja": motivo,
                    "fecha_baja": datetime.datetime.now().isoformat()
                }
            }
        )

        if resultado.matched_count == 0:
            return "Error: DNI no encontrado en la base de datos o usuario ya está dado de baja."
        return f"Success: Usuario {dni} dado de baja. Motivo registrado: {motivo}"

    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if client: client.close()
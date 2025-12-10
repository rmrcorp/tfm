# Archivo: src/mcp/debug_utils.py
import sys
import functools
import json
import os
import datetime

# CAMBIO: Usamos getcwd() para que el fichero aparezca SIEMPRE
# en la carpeta desde donde lanzas el terminal (la raíz del proyecto).
LOG_FILE = os.path.join(os.getcwd(), 'mcp_debug.log')


def write_log(message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    log_line = f"[{timestamp}] {message}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception as e:
        sys.stderr.write(f"ERROR LOGGING: {e}\n")

    sys.stderr.write(log_line)

def log_mcp(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            write_log(f"[OK] '{func.__name__}' | Return: {str(result)[:100]}...")
            return result
        except Exception as e:
            write_log(f"[ERROR] en '{func.__name__}': {str(e)}")
            raise e

    return wrapper
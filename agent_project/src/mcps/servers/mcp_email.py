import sys

from src.mcps.utils.log_mcp import log_mcp


@log_mcp
def enviar_email(destinatario: str, asunto: str, cuerpo: str) -> str:
    """
    Envía un correo electrónico a un destinatario.

    USO OBLIGATORIO EN:
        1. Comunicados en los procesos.

    El Asistente (tú) es responsable de redactar un 'cuerpo' profesional y completo basado en el contexto.
    ARGS:
    - destinatario: Dirección de email del receptor (ej: cliente@empresa.com).
    - asunto: El título o subject del correo.
    - cuerpo: El contenido completo del mensaje (texto plano).
    """
    sys.stderr.write(f"\n --- SIMULANDO ENVÍO SMTP ---")
    sys.stderr.write(f"TO: {destinatario}")
    sys.stderr.write(f"SUBJECT: {asunto}")
    sys.stderr.write(f"BODY:\n{cuerpo}")


    return f"Success: Correo enviado a '{destinatario}' con asunto '{asunto}'."
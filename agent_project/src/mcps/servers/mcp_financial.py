import sys

from src.mcps.utils.log_mcp import log_mcp


@log_mcp
def consultar_solvencia_credito(dni: str) -> str:
    """
    Consulta el Scoring Financiero y deudas pendientes.

    USO:
    - Ejecutar OBLIGATORIAMENTE antes de dar de Alta (para ver si es apto).
    - Ejecutar OBLIGATORIAMENTE antes de dar de Baja (para ver si tiene deuda cero).

    RETORNO:
    - Devuelve "APTO" si el cliente está limpio.
    - Devuelve "NO APTO" o "DEUDA PENDIENTE" si hay problemas.

    NOTA: El agente debe LEER el resultado y DETENER el proceso si es negativo.
    """
    sys.stderr.write("Ejecutando consulta el Scoring Financiero")
    # --- SIMULACIÓN PARA TESTEO ---
    # Si el DNI termina en '9', simulamos que es moroso.
    if dni.strip()[-1] == '9':
        return f"RESULTADO: NO APTO. El DNI {dni} tiene incidencias en ASNEF/RAI. Deuda pendiente: 1.500€."

    return f"RESULTADO: APTO. Solvencia verificada. Scoring Verde. Deuda Cero."


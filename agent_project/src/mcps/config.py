import sys
import os
from mcp import StdioServerParameters

# Configuración del servidor MCP
server_params = StdioServerParameters(
    command=sys.executable,
    args=["src/mcps/mcp_server.py"],
    env={**os.environ, "PYTHONPATH": os.getcwd()}
)

JAVA_SSE_URL = "http://localhost:8080/sse"
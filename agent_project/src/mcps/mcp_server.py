from mcp.server.fastmcp import FastMCP
import sys
import os

from src.mcps.servers.mcp_financial import consultar_solvencia_credito

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.mcps.servers.mcp_bbdd import init_db, guardar_cliente_db, baja_cliente_db
from src.mcps.servers.mcp_email import enviar_email

mcp = FastMCP("AgenteCorporativoBPM", dependencies=["pymongo"])
mcp.add_tool(consultar_solvencia_credito)
mcp.add_tool(guardar_cliente_db)
mcp.add_tool(baja_cliente_db)
mcp.add_tool(enviar_email)

if __name__ == "__main__":
    try:
        init_db()
        mcp.run(transport='stdio')
    except Exception as e:
        sys.stderr.write(f"!!! ERROR al arrancar los MCP: {e}")
        sys.exit(1)

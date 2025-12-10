import asyncio
import sys
import os
from contextlib import AsyncExitStack
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

from src.agent.agent import build_agent
from src.mcps.mcp_mapping import mapping_mcp_stdout_tools, mapping_mcp_http_tools
from src.rag.rag_index import index_process_files

# Configuración del servidor MCP
server_params = StdioServerParameters(
    command=sys.executable,
    args=["src/mcps/mcp_server.py"],
    env={**os.environ, "PYTHONPATH": os.getcwd()}
)

EXIT_INSTRUCTIONS = ['salir', 'exit', 'quit']
JAVA_SSE_URL = "http://localhost:8080/sse"

async def main():
    print("==== Iniciando Agente Experto (Ollama + qwen2.5:32b + MCPs) ====")
    try:
        index_process_files()
    except Exception as e:
        print(f"!!! Error en RAG (Cerramos Agente, no se puede continuar sin acceso a los procesos) !!!: {e}")
        sys.exit(1)

    print("Conectando con servidor MCP...")
    async with AsyncExitStack() as stack:
        # 1. Conexión Python
        print("Conectando (Stdio)...")
        read_py, write_py = await stack.enter_async_context(stdio_client(server_params))
        session_stdout = await stack.enter_async_context(ClientSession(read_py, write_py))
        await session_stdout.initialize()

        # 2. Conexión Http (Java Spring CRM)
        print(f"Conectando http CRM ({JAVA_SSE_URL})...")
        read_java, write_java = await stack.enter_async_context(sse_client(JAVA_SSE_URL, timeout=10.0, sse_read_timeout=None))
        session_http_crm = await stack.enter_async_context(ClientSession(read_java, write_java))
        await session_http_crm.initialize()

        tools = await session_http_crm.list_tools()
        print(f"LISTA DE HERRAMIENTAS HTTP: {[t.name for t in tools.tools]}")

        print("Configurando Herramientas...")

        tools_from_stdout = mapping_mcp_stdout_tools(session_stdout)
        tools_from_http = mapping_mcp_http_tools(session_http_crm)
        all_tools = tools_from_stdout + tools_from_http

        print(f"Herramientas que comunican por consola (stdout): {len(tools_from_stdout)}")
        print(f"Herramientas que comunican por http: {len(tools_from_http)}")
        print(f"Total: {len(all_tools)}")

        app = build_agent(all_tools)

        config = {"configurable": {"thread_id": "user_session"}}

        while True:
            try:
                user_input = input("\033[1;34mUsuario:\033[0m ")
                if user_input.lower() in EXIT_INSTRUCTIONS: break
                inputs = {"messages": [("human", user_input)]}
                async for event in app.astream(inputs, config=config, stream_mode="values"):
                    await _show_last_ia_message(event)

            except KeyboardInterrupt:
                print("Saliendo...")
                break

async def _show_last_ia_message(event: dict[str, Any] | Any):
    last_msg = event["messages"][-1]
    if last_msg.type == "ai":
        if last_msg.tool_calls:
            tools_used = [t['name'] for t in last_msg.tool_calls]
            print(f"Usando MCP con el nombre: {tools_used}")
        elif last_msg.content:
            print(f"\033[1;32mAgente:\033[0m {last_msg.content}")


def _windows_hack():
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


if __name__ == "__main__":
    _windows_hack()
    asyncio.run(main())
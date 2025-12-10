from langchain_core.tools import StructuredTool
from mcp import ClientSession

from src.mcps.mcp_definition import SolvenciaInput, GuardarClienteInput, BajaClienteInput, EmailInput, CrmJavaInput


def mapping_mcp_stdout_tools(session: ClientSession) -> list[StructuredTool]:
    async def call_mcp_stdout_tool(tool_name: str, **kwargs):
        return await session.call_tool(tool_name, arguments=kwargs)

    tool_solvencia = StructuredTool.from_function(
        coroutine=lambda **kwargs: call_mcp_stdout_tool("consultar_solvencia_credito", **kwargs),
        name="consultar_solvencia_credito",
        description="[OBLIGATORIO] Consulta si un cliente tiene deudas o es apto financiero.",
        args_schema=SolvenciaInput
    )

    tool_guardar = StructuredTool.from_function(
        coroutine=lambda **kwargs: call_mcp_stdout_tool("guardar_cliente_db", **kwargs),
        name="guardar_cliente_db",
        description="Registra al cliente en BBDD. Requiere 'consultar_solvencia_credito' previo.",
        args_schema=GuardarClienteInput
    )

    tool_baja = StructuredTool.from_function(
        coroutine=lambda **kwargs: call_mcp_stdout_tool("baja_cliente_db", **kwargs),
        name="baja_cliente_db",
        description="Da de baja a un cliente activo en base de datos.",
        args_schema=BajaClienteInput
    )

    tool_email = StructuredTool.from_function(
        coroutine=lambda **kwargs: call_mcp_stdout_tool("enviar_email", **kwargs),
        name="enviar_email",
        description="Envía correos electrónicos para los procesos que lo requieran o "
                    "cuando se indique en algún sitio que se tiene qu enviar un email, "
                    "(Bienvenida, Bajas, Notificaciones)."
                    "Enviar comunicados",
        args_schema=EmailInput
    )

    return [tool_baja, tool_email, tool_guardar, tool_solvencia]


def mapping_mcp_http_tools(session: ClientSession) -> list[StructuredTool]:
    async def call_mcp_http_tools(tool_name: str, **kwargs):
        return await session.call_tool(tool_name, arguments=kwargs)

    # IMPORTANTE: El 'name' debe coincidir con el nombre del @Bean en Java
    # Si en Java pusiste @Bean public Function... crear_usuario_crm
    # Aquí debe ser "crear_usuario_crm".
    return [
        StructuredTool.from_function(
            coroutine=lambda **kwargs: call_mcp_http_tools("sincronizarUsuarioCRM", **kwargs),
            name="sincronizarUsuarioCRM",
            description="Sincroniza un usuario a travé del dni al CRM.",
            args_schema=CrmJavaInput
        )
    ]

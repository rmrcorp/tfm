from enum import Enum
from typing import Annotated, TypedDict, List

from langgraph.graph import add_messages
from pydantic import BaseModel, Field

class AgentState(TypedDict):
    messages: Annotated[list, add_messages] # mensajes acumulados (como MessageState de LangGraph)
    context: str # aquí se carga el proceso que se ha solicitado (documento procedente del RAG)
    intention: str

class IntentCategory(str, Enum):
    PROVIDE_DATA = "provide_data"
    ASK_CAPABILITIES = "ask_capabilities"
    QUERY_PROCESS = "query_process"
    GENERAL_CHAT = "general_chat"
    CONTEXT_CHAT = "context_chat"


class UserIntent(BaseModel):
    category: IntentCategory = Field(
        description="Categoría de la intención del usuario"
    )
    reasoning: str = Field(description="Breve explicación de por qué has elegido esta categoría")


class ExecutionPlan(BaseModel):
    """Estructura para definir el plan de ejecución de un proceso."""
    process_name: str = Field(..., description="Nombre del proceso identificado en el RAG (ej: 'Alta Cliente').")
    steps: List[str] = Field(..., description="Lista ordenada de pasos OBLIGATORIOS extraídos del RAG.")
    rationale: str = Field(..., description="Breve explicación de por qué son necesarios estos pasos.")


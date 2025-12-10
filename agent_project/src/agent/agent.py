from typing import List

from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage

from src.agent.agent_planner import planning_node
from src.agent.agent_state import AgentState, IntentCategory
from src.agent.model import llm
from src.agent.user_intention import get_user_intent
from src.rag.rag_engine import find_context, get_master_index
from langgraph.checkpoint.memory import MemorySaver

def build_agent(mcp_tools: List):
    llm_with_tools = llm.bind_tools(mcp_tools)

    def context_node(state: AgentState):
        # 1. Obtenemos la intención (Llamada al LLM)
        decision = get_user_intent(state)
        # 2. Obtenemos mensaje actual y contexto actual para pasar obtener nuevo contexto..
        last_msg = state["messages"][-1].content
        current_ctx = state.get("context", "")
        # 3. Ejecutamos la acción (Lógica Python)
        nuevo_contexto = resolve_context_by_intent(decision.category, last_msg, current_ctx)
        # 4. Actualizamos el estado
        return {
            "context": nuevo_contexto,
            "intention": decision.category  # <--- IMPORTANTE: Guardamos la etiqueta (QUERY_PROCESS, etc.)
        }

    def agent_node(state: AgentState):
        current_context = state.get("context", "")

        prompt_content = f"""Eres un Asistente de Procesos BPM experto. Tu trabajo NO es ejecutar comandos a ciegas, sino GUIAR al usuario para finalizar un proceso completo del RAG.

        CONTEXTO DE REGLAS DE NEGOCIO (RAG):
        ---------------------------------------------------
        {current_context}
        ---------------------------------------------------

        ESTADO ACTUAL:
        El usuario quiere realizar una acción. Tú debes verificar si tienes TODOS los datos necesarios según el CONTEXTO DE REGLAS DE NEGOCIO de arriba.

        ALGORITMO DE PENSAMIENTO (Sigue estos pasos):
        0. ¿Tengo contexto nuevo?
            - SI -> Muestra los las fases de las que se compone el proceso
            - NO -> continua
        1. ¿Tengo contexto del proceso? 
           - SI -> Ve al paso 2.
           - NO -> Di que no puedes ayudar.

        2. ¿El usuario me ha dado YA todos los datos obligatorios en el chat para continuar el proceso?
           - NO -> ¡DETENTE! NO LLAMES A NINGUNA HERRAMIENTA.
             Tu respuesta DEBE SER una pregunta pidiendo los datos que faltan.
             Ejemplo: "Para proceder con el alta, necesito que me indiques el DNI y el Nombre completo."

           - SI (Solo si los ha escrito explícitamente) -> Entonces sí, llama a la herramienta correspondiente.

        PROHIBICIONES:
        - PROHIBIDO inventar nombres (Ej: Juan Pérez), DNIs o Emails.
        - PROHIBIDO asumir datos que no están en el chat.
        - PROHIBIDO ejecutar la herramienta si falta aunque sea UN solo dato.
        - PROHIBIDO acabar sin ejecutar todas las fases.
        - PROHIBIDO alterar el orden de las Fases.
      
        Es OBLIGATORIO realizar todas las fases del proceso en el orden que están.
        
        REGLA DE ORO DE CONTINUIDAD:
            Cuando el contexto RAG describa un procedimiento con múltiples pasos secuenciales (Fases, Etapas, Pasos):
            1. Antes de actuar, PLANIFICA mentalmente todos los pasos necesarios según el documento y ordenalos según proceda.
            2. INFORMA de las fases que tiene el proceso que se va a ejecutar.
            3. EJECUTA todas las herramientas necesarias para cubrir TODAS las fases descritas en el texto.
            4. PROHIBIDO detenerse o responder al usuario a mitad del proceso para confirmar "éxito parcial".
            5. Si una herramienta devuelve "OK", tu obligación es consultar en el conetxto que has obtenido del RAG, ver cuál es la SIGUIENTE fase y ejecutarla inmediatamente.
            6. Solo cuando hayas completado la ÚLTIMA fase descrita en el documento, podrás responder al usuario.
            7. Finaliza solo cuando ejecutes el ÚLTIMO paso, nunca digas que has finalizado sin completar todas las fases.

        Responde en Español natural y profesional.
        """

        sys_msg = SystemMessage(content=prompt_content)
        messages = [sys_msg] + state["messages"]

        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    # Construcción del Grafo
    workflow = StateGraph(AgentState) # grafo vacío donde se le pasa la clase state que se usará (AgentState)

    # Definimos los nodos de los que se compondrá el workflow.
    workflow.add_node("retrieve", context_node)
    workflow.add_node("planner", planning_node)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(mcp_tools))

    # primer paso: comprobamos la intención del usuario y contextualizamos al agente
    workflow.add_edge(START, "retrieve")
    # RAG -> Planificador (Aquí se decide qué hacer)
    #workflow.add_edge("retrieve", "planner")
    workflow.add_conditional_edges(
        "retrieve",  # Desde el nodo retrieve...
        _router_by_intention,  # ...ejecuta esta función lógica...
        {
            "planner": "planner",  # Si devuelve 'planner' -> ve al nodo planner
            "agent": "agent"  # Si devuelve 'agent' -> sáltatelo y ve al agente
        }
    )
    workflow.add_edge("planner", "agent")
    workflow.add_conditional_edges("agent", tools_condition)
    workflow.add_edge("tools", "agent")

    memory = MemorySaver()

    # Compilamos pasando el checkpointer
    return workflow.compile(checkpointer=memory)

def resolve_context_by_intent(intention: str, user_msg: str, current_context: str) -> str:
    if intention == IntentCategory.PROVIDE_DATA:
        print("ACCIÓN: Mantener contexto (Input de datos).")
        return current_context

    elif intention == IntentCategory.ASK_CAPABILITIES:
        print("ACCIÓN: Cargar Índice Maestro (Menú).")
        return get_master_index()

    elif intention == IntentCategory.QUERY_PROCESS:
        print("ACCIÓN: Búsqueda Vectorial (RAG).")
        new_context = find_context(user_msg)
        if new_context:
            return new_context
        else:
            return current_context  # Si no encuentra nada, mantiene lo anterior

    elif intention == IntentCategory.GENERAL_CHAT:
        print("ACCIÓN: Charla general. Limpiar contexto.")
        return ""  # Limpiamos contexto para charlar ligero

    elif intention == IntentCategory.CONTEXT_CHAT:
        print("ACCIÓN: Charla contextualizada.")
        return current_context

    return ""


from typing import Literal


def _router_by_intention(state: AgentState) -> Literal["planner", "agent"]:
    intention = state.get("intention", "CHAT")
    context = state.get("context", "")
    if intention == "QUERY_PROCESS" and context:
        return "planner"
    return "agent"
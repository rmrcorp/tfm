from langchain_core.prompts import ChatPromptTemplate
from src.agent.agent_state import AgentState, UserIntent
from src.agent.model import llm_user_intention

def get_user_intent(state: AgentState) -> UserIntent:
    messages = state["messages"]
    last_user_msg = messages[-1].content

    # Obtener contexto inmediato (mensaje anterior de la IA)
    last_ai_msg = "Ninguno (Inicio de conversación)"
    ai_msgs = [m for m in messages if m.type == "ai"]
    if ai_msgs:
        last_ai_msg = ai_msgs[-1].content

    system_prompt = """Eres un Router de Clasificación de Intenciones.
    Analiza la conversación y clasifica el último mensaje del usuario.

    CATEGORÍAS:
    1. 'provide_data': Usuario da un dato corto (DNI, Nombre, 'sí', 'no') respondiendo al Asistente.
    2. 'ask_capabilities': Pregunta qué puede hacer el bot (Menú, Ayuda).
    3. 'query_process': Quiere iniciar o consultar un proceso (Alta, Baja, Requisitos).
    4. 'general_chat': Saludos, gracias, fuera de contexto.
    5. 'context_chat': Usuario restá preguntando sobre acciones o conversaciones pasadas, que ha hecho hace poco.

    CONTEXTO:
    - Asistente dijo: "{last_ai_msg}"
    - Usuario dijo: "{user_input}"
    """

    prompt = ChatPromptTemplate.from_template(system_prompt)
    router_chain = prompt | llm_user_intention

    print(f"USER INTENTION: Analizando: '{last_user_msg}'...")

    try:
        decision = router_chain.invoke({
            "last_ai_msg": last_ai_msg,
            "user_input": last_user_msg
        })
        print(f"DECISIÓN LLM: {decision.category.upper()} (Razón: {decision.reasoning})")
        return decision

    except Exception:
        print(f"!!! Error analizando la intención del usuario, por defecto se ejecuta una \"query_process\"")
        return UserIntent(category="query_process", reasoning="Error en LLM, fallback por defecto.")
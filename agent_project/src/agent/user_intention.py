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



# PROMPT ANTERIOR
    """

    system_prompt = Eres un experto analista de intenciones en un sistema de chat de Procesos de Negocio.
        Tu único trabajo es clasificar el último mensaje del usuario en una de estas 4 categorías:

        1. 'provide_data': El usuario está proporcionando un dato corto (DNI, Nombre, Email, Motivo, Confirmación) 
           que probablemente le ha pedido el Asistente en el mensaje anterior.
           Ejemplos: "Ruben", "12345678H", "baja voluntaria", "sí", "no".

        2. 'ask_capabilities': El usuario pregunta qué puede hacer el bot o qué procesos existen.
           Ejemplos: "¿Qué haces?", "Menú", "Lista de procesos", "Ayuda".

        3. 'query_process': El usuario quiere iniciar o consultar información sobre un proceso de negocio específico.
           Ejemplos: "Quiero dar de alta", "Cómo doy de baja", "Requisitos para alta".

        4. 'general_chat': Saludos, despedidas o frases fuera de contexto de negocio.
           Ejemplos: "Hola", "Buenos días", "Gracias".
           
        5. ANTI-BUCLE: Antes de llamar a una herramienta, mira el historial. ¿Acabas de llamarla con los mismos datos? Si es sí, DETENTE.
        6. FORMATO: NO escribas JSON en el chat. Ejecuta la herramienta de forma oculta (Native Tool Call).
        7. FINALIZACIÓN: Si la herramienta devuelve "Éxito", TU TRABAJO HA TERMINADO. No vuelvas a llamar a la herramienta. Informa al usuario y calla.

        ANALIZA EL CONTEXTO:
        - Último mensaje del Asistente: "{last_ai_msg}"
        - Último mensaje del Usuario: "{user_input}"
        
    
    """
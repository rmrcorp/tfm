"""
        Router Semántico (LLM):
        Analiza la intención real del usuario basándose en la conversación
        para decidir si buscar en RAG, listar menú o mantener el foco.
        """
messages = state["messages"]
last_user_msg = messages[-1].content

# 1. OBTENER CONTEXTO INMEDIATO (¿Qué dijo la IA justo antes?)
# Esto es CRUCIAL para distinguir si el usuario está respondiendo a una pregunta.
last_ai_msg = "Ninguno (Inicio de conversación)"
ai_msgs = [m for m in messages if m.type == "ai"]
if ai_msgs:
    last_ai_msg = ai_msgs[-1].content

# 3. PROMPT DE CLASIFICACIÓN
system_prompt = """Eres un experto analista de intenciones en un sistema de chat de Procesos de Negocio.
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

prompt = ChatPromptTemplate.from_template(system_prompt)

# Creamos la cadena
router_chain = prompt | llm_user_intention

# 4. EJECUTAR CLASIFICACIÓN
print(f"🧠 ROUTER: Analizando intención de '{last_user_msg}'...")
try:
    decision = router_chain.invoke({
        "last_ai_msg": last_ai_msg,
        "user_input": last_user_msg
    })
    intent = decision.category
    print(f"DECISIÓN LLM: {intent.upper()} (Razón: {decision.reasoning})")

except Exception as e:
    # Fallback por si el LLM falla al generar JSON (raro en Llama 3.1)
    print(f"!!! Error en Router LLM: {e}. Usando fallback heurístico.")
    intent = "query_process"  # Asumimos búsqueda por defecto

 async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("Configurando MCPs...")
            langchain_tools = mapping_mcp_tools(session)
            print(f"MCPs conectados y mapeados: {len(langchain_tools)}")

            app = build_agent(langchain_tools)
            print("Sistema listo. Escribe 'salir' para terminar.")

            # this is the agent memory.
            config = {"configurable": {"thread_id": "user_session"}}

            while True:
                try:
                    user_input = input("Usuario: ")
                    if user_input.lower() in EXIT_INSTRUCTIONS: break
                    inputs = {"messages": [("human", user_input)]}
                    async for event in app.astream(inputs, config=config, stream_mode="values"):
                        await _show_last_ia_message(event)

                except KeyboardInterrupt:
                    print("Saliendo...")
                    break




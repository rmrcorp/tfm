from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

from src.agent.agent_state import AgentState, ExecutionPlan
from src.agent.model import llm_planner


def planning_node(state: AgentState):
    planner_prompt = ChatPromptTemplate.from_template(
        """ERES UN AUDITOR DE PROCESOS RIGUROSO.

        TU TAREA:
        Analiza el siguiente DOCUMENTO OFICIAL (RAG) y extrae los pasos para responder a la solicitud del usuario.

        DOCUMENTO OFICIAL (CONTEXTO):
        ---------------------------------------------
        {context}
        ---------------------------------------------

        INSTRUCCIONES DE VISIÓN DE TÚNEL (SÍGUELAS O FALLARÁS):
        1. Ignora completamente la sección "Requisitos Previos" o "Datos Obligatorios". Esos NO son pasos, son datos.
        2. Tu objetivo es encontrar los encabezados que digan "FASE X" o "PASO X".
        3. Si el documento dice explícitamente "El proceso consta de 5 fases", tu salida DEBE tener 5 pasos.
        4. No resumas. Usa el nombre exacto de la fase (ej: "Evaluación de Riesgos").
        
        EJEMPLO DE LO QUE BUSCO:
        Si el texto dice:
        "FASE 1: Recopilación... FASE 2: Scoring... FASE 3: Base de Datos..."
        
        Tu salida debe ser un listado de las fases a ejecutar.

        Genera el plan de ejecución estructurado ahora:
        """
    )

    chain = planner_prompt | llm_planner
    try:
        # 4. INVOCAMOS PASANDO EL CONTEXTO EXPLÍCITAMENTE
        plan: ExecutionPlan = chain.invoke({
            "context": state["context"]
        })
        # Formatear el plan para el historial
        plan_text = f"PLAN BASADO EN DOCUMENTACIÓN OFICIAL ({plan.process_name}):\n"
        for i, step in enumerate(plan.steps, 1):
            plan_text += f"{i}. {step}\n"
        return {
            "messages": [AIMessage(content=plan_text)]
        }

    except Exception as e:
        print(f"Error en planner: {e}")
        return {"messages": [SystemMessage(content="Error generando plan.")]}
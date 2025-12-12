import asyncio
import time

from datetime import datetime

from langchain_core.messages import HumanMessage, AIMessage

from src.agent.agent import get_user_intent
from src.agent.agent_state import AgentState
from test.agent.intent_config import TEST_CASES_FILE, NUM_ITERATIONS_METRICS, OUTPUT_FILE
from test.utils.file_utils import load_cases, store_summary
from test.utils.resource_monitor_model import ResourceMonitor


def create_mock_agent_state(user_input: str, last_ai_msg: str) -> AgentState:
    messages = []
    if last_ai_msg and last_ai_msg.strip():
        messages.append(AIMessage(content=last_ai_msg))
    messages.append(HumanMessage(content=user_input))
    return AgentState(
        messages=messages,
        context="",
        intention=""
    )

async def execute_benchmark():
    print(f"Benchmark Intención del usuario - {datetime.now()}")
    cases = load_cases(TEST_CASES_FILE)
    if not cases: return

    resultados_csv = []

    for group in cases:
        group_id = group['id']
        expected_cat = group['expected_category']  # String: "provide_data"
        test_cases = group['cases']

        print(f"\n{'=' * 60}")
        print(f"GRUPO: {group_id} | Esperado: '{expected_cat.upper()}'")
        print(f"{'=' * 60}")

        stats_grupo = {'exitos': 0, 'total': 0, 'latencias': []}

        for case in test_cases:
            user_input = case['user_input']
            ai_context = case.get('last_ai_msg', "")

            mock_state = create_mock_agent_state(user_input, ai_context)

            latencies = []
            cat_result_str = "ERROR"  # El string final para comparar
            reasoning = ""

            monitor = ResourceMonitor()
            monitor.start()

            for _ in range(NUM_ITERATIONS_METRICS):
                start = time.time()
                try:
                    decision_obj = get_user_intent(mock_state)
                    if decision_obj and hasattr(decision_obj, 'category'):
                        cat_result_str = decision_obj.category.value
                        reasoning = decision_obj.reasoning
                    else:
                        cat_result_str = "None"

                except Exception as e:
                    cat_result_str = f"ERROR: {e}"

                latencies.append(time.time() - start)

            avg_cpu, max_ram = monitor.stop()
            monitor.join()

            # Validación (Comparar String vs String)
            es_exito = (cat_result_str.lower() == expected_cat.lower())

            # Stats
            stats_grupo['total'] += 1
            if es_exito: stats_grupo['exitos'] += 1
            lat_avg = sum(latencies) / len(latencies)
            stats_grupo['latencias'].append(lat_avg)

            # --- VISUALIZACIÓN ---
            result_text = "\033[92mOK\033[0m" if es_exito else "\033[91mFAIL\033[0m"

            print(f"User: \"{user_input}\"")
            print(f"Ctx : \"{ai_context[:40]}...\"")
            print(f"{cat_result_str} {result_text} | Razón: {reasoning[:60]}...")
            print(f" {lat_avg:.3f}s | RAM: {max_ram:.1f}MB\n")

            resultados_csv.append({
                "Group": group_id,
                "User_Input": user_input,
                "Context": ai_context,
                "Expected": expected_cat,
                "Obtained": cat_result_str,
                "Reasoning": reasoning,
                "Success": 1 if es_exito else 0,
                "Latency": lat_avg,
                "RAM_Max": max_ram
            })

        acc = (stats_grupo['exitos'] / stats_grupo['total'] * 100) if stats_grupo['total'] else 0
        lat_g = sum(stats_grupo['latencias']) / len(stats_grupo['latencias']) if stats_grupo['latencias'] else 0
        print(f"RESUMEN {group_id}: Precisión: {acc:.0f}% | Latencia Media: {lat_g:.3f}s")

    await store_summary(resultados_csv, OUTPUT_FILE)


if __name__ == "__main__":
    asyncio.run(execute_benchmark())
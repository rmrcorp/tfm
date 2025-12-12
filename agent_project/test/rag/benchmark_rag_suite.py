import asyncio
import time

from datetime import datetime

from src.rag.rag_engine import detect_document_target
from test.rag.rag_test_config import TEST_CASES_FILE, NUM_ITERATIONS_METRICS, OUTPUT_FILE

from test.utils.file_utils import store_summary, load_cases
from test.utils.resource_monitor_model import ResourceMonitor, print_summary


async def execute_benchmark():
    print(f"Benchmark RAG - {datetime.now()}")
    cases = load_cases(TEST_CASES_FILE)
    if not cases:
        print("ERROR: No test cases found.")
        return

    results = []

    for case in cases:
        case_id = case['id']
        expected_document = case['doc_esperado']
        prompts = case['prompts']

        print(f"\n{'=' * 50}")
        print(f"GRUPO: {case_id} | Esperado: '{expected_document}'")
        print(f"{'=' * 50}")

        stats_grupo = {'exitos': 0, 'total': 0, 'latencias': []}

        for prompt in prompts:

            prompt_latencies = []
            final_prompt_result = ""

            monitor = ResourceMonitor()
            monitor.start()

            for _ in range(NUM_ITERATIONS_METRICS):
                start = time.time()
                try:
                    res = detect_document_target(prompt)
                    final_prompt_result = res
                except Exception:
                    final_prompt_result = "ERROR"
                prompt_latencies.append(time.time() - start)

            avg_cpu, max_ram = monitor.stop()
            monitor.join()

            is_success = expected_document in final_prompt_result

            stats_grupo['total'] += 1
            if is_success: stats_grupo['exitos'] += 1
            latencia_media = sum(prompt_latencies) / len(prompt_latencies)
            stats_grupo['latencias'].append(latencia_media)

            # --- IMPRIMIR RESULTADO DEL PROMPT  ---
            result_text = "\033[92mOK\033[0m" if is_success else "\033[91mFAIL\033[0m"
            print(f"Prompt: \"{prompt}\"")
            print(f"Resultado: {final_prompt_result} {result_text} | {latencia_media:.3f}s")

            results.append({
                "Case_ID": case_id,
                "Prompt": prompt,
                "Esperado": expected_document,
                "Obtenido": final_prompt_result,
                "Exito": 1 if is_success else 0,
                "Latencia": latencia_media,
                "CPU_Avg": round(avg_cpu, 2),
                "RAM_Max": round(max_ram, 2)
            })

        await print_summary(case_id, stats_grupo)
    await store_summary(results, OUTPUT_FILE)



if __name__ == "__main__":
    asyncio.run(execute_benchmark())
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_CASES_DIR = os.path.dirname(BASE_DIR) # Carpeta 'test'
TEST_CASES_FILE = os.path.join(TEST_CASES_DIR, "rag/benchmark_rag_suite_test_cases.json")

NUM_ITERATIONS_METRICS = 5
OUTPUT_FILE = "resultados_rag.csv"
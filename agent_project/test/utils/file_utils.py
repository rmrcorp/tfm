import json
import os
from typing import Any

import pandas as pd


def load_cases(ruta):
    if not os.path.exists(ruta): return []
    with open(ruta, 'r', encoding='utf-8') as f: return json.load(f)


async def store_summary(resultados_csv: list[Any], output_file: str):
    pd.DataFrame(resultados_csv).to_csv(output_file, index=False)
    print(f"\nCSV generado en: {output_file}")
import os
import threading
import time
from typing import Any

import psutil


class ResourceMonitor(threading.Thread):
    def __init__(self, interval=0.1):
        super().__init__()
        self.interval = interval
        self.running = True
        self.cpu_usage = []
        self.ram_usage = []
        self.process = psutil.Process(os.getpid())

    def run(self):
        while self.running:
            self.cpu_usage.append(psutil.cpu_percent(interval=None))
            try:
                self.ram_usage.append(self.process.memory_info().rss / 1024 / 1024)
            except:
                pass
            time.sleep(self.interval)

    def stop(self):
        self.running = False
        avg_cpu = sum(self.cpu_usage) / len(self.cpu_usage) if self.cpu_usage else 0
        max_ram = max(self.ram_usage) if self.ram_usage else 0
        return avg_cpu, max_ram


async def print_summary(case_id, stats_grupo: dict[str, int | list[Any]]):
    accuracy = (stats_grupo['exitos'] / stats_grupo['total']) * 100
    global_latency = sum(stats_grupo['latencias']) / len(stats_grupo['latencias'])
    print(f"\nRESUMEN {case_id}: Precisión: {accuracy:.0f}% | Latencia Media: {global_latency:.3f}s")
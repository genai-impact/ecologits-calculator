from __future__ import annotations

import json
from pathlib import Path

_BASE_PATH = Path(__file__).parent / "data" / "throughputs.json"


class LatencyEstimator:
    __DEFAULT_TPS = 80.0

    def __init__(self, file_path: str | Path) -> None:
        with open(file_path, "r") as fd:
            data = json.load(fd)

        self.__throughputs = {}
        for el in data["models"]:
            self.__throughputs[(el["provider"], el["name"])] = el["throughput"]

    def get_throughput(self, provider: str, model_name: str) -> float:
        return float(self.__throughputs.get((provider, model_name), self.__DEFAULT_TPS))

    def estimate(self,
                 provider: str,
                 model_name: str,
                 output_tokens: int,
                 throughput: float | None = None) -> float:
        if throughput is None:
            throughput = self.__throughputs.get((provider, model_name), self.__DEFAULT_TPS)
        return float(output_tokens / throughput)


latency_estimator = LatencyEstimator(file_path=_BASE_PATH)

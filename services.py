import json
from datetime import datetime
from typing import List

from fastapi import HTTPException
from pydantic import ValidationError

from schemas import BenchmarkAveragePerformance, BenchmarkResult


class SuperBenchmarkService:

    def __init__(self, debug_mode: bool):
        self.debug_mode = debug_mode
        self.benchmarking_results = self.load_data()

    def load_data(self) -> List[BenchmarkResult]:
        if self.debug_mode:
            try:
                with open("test_database.json", "r") as f:
                    data = json.load(f)
                    return [
                        BenchmarkResult(**item) for item in data["benchmarking_results"]
                    ]
            except FileNotFoundError:
                raise HTTPException(
                    status_code=500, detail="test_database.json file not found."
                )
            except ValidationError as e:
                raise HTTPException(
                    status_code=500, detail=f"Data validation error: {e}"
                )
        else:
            raise HTTPException(
                status_code=501, detail="Feature is not ready for live yet."
            )

    def compute_average_performance(
        self, results: List[BenchmarkResult] | None = None
    ) -> BenchmarkAveragePerformance:
        results = results or self.benchmarking_results
        total_token_count = 0
        total_time_to_first_token = 0
        total_time_per_output_token = 0
        total_total_generation_time = 0
        for result in results:
            total_token_count += result.token_count
            total_time_to_first_token += result.time_to_first_token
            total_time_per_output_token += result.time_per_output_token
            total_total_generation_time += result.total_generation_time
        result_count = len(results)
        if result_count == 0:
            return BenchmarkAveragePerformance()
        return BenchmarkAveragePerformance(
            average_token_count=total_token_count / result_count,
            average_time_to_first_token=total_time_to_first_token / result_count,
            average_time_per_output_token=total_time_per_output_token / result_count,
            average_total_generation_time=total_total_generation_time / result_count,
        )

    def get_average_performance(self) -> BenchmarkAveragePerformance:
        return self.compute_average_performance()

    def get_average_performance_in_window(
        self, start_time: datetime, end_time: datetime
    ) -> BenchmarkAveragePerformance:
        results_in_window = [
            result
            for result in self.benchmarking_results
            if start_time <= result.timestamp <= end_time
        ]
        return self.compute_average_performance(results_in_window)

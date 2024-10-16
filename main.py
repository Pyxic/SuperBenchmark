from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Path

from dependencies import superbenchmark_service
from services import SuperBenchmarkService

app = FastAPI()


@app.get("/results/average")
def get_average_performance_statistics(
    benchmark_service: SuperBenchmarkService = Depends(superbenchmark_service),
):
    return benchmark_service.get_average_performance()


@app.get("/results/average/{start_time}/{end_time}")
def say_hello(
    start_time: datetime = Path(..., description="Start time in ISO 8601 format"),
    end_time: datetime = Path(..., description="End time in ISO 8601 format"),
    benchmark_service: SuperBenchmarkService = Depends(superbenchmark_service),
):
    if start_time > end_time:
        raise HTTPException(
            status_code=400, detail="start_time must be before or equal to end_time"
        )
    return benchmark_service.get_average_performance_in_window(start_time, end_time)

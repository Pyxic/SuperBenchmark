from datetime import datetime

from pydantic import BaseModel


class BenchmarkResult(BaseModel):
    request_id: str
    prompt_text: str
    generated_text: str
    token_count: int
    time_to_first_token: int  # in milliseconds
    time_per_output_token: int  # in milliseconds
    total_generation_time: int  # in milliseconds
    timestamp: datetime


class BenchmarkAveragePerformance(BaseModel):
    average_token_count: float = 0
    average_time_to_first_token: float = 0
    average_time_per_output_token: float = 0
    average_total_generation_time: float = 0

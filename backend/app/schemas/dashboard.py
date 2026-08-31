from typing import Dict, List, Optional
from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_projects: int
    total_datasets: int
    active_training_jobs: int
    completed_training_jobs: int
    failed_training_jobs: int
    registered_models: int
    deployed_models: int
    total_api_requests: int
    avg_model_accuracy: float
    system_cpu_usage_pct: float
    system_memory_usage_pct: float


class ChartSeriesItem(BaseModel):
    name: str
    data: List[float]


class ChartDataResponse(BaseModel):
    categories: List[str]
    series: List[ChartSeriesItem]

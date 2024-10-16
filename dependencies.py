from services import SuperBenchmarkService
from settings import settings


def superbenchmark_service():
    return SuperBenchmarkService(settings.debug)

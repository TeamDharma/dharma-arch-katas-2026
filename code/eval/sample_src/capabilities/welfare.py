"""Animal welfare anomaly detection. Gateway only."""
from gateway.model_gateway import complete


def assess(readings: dict) -> dict:
    return {"concern": complete("animal-welfare", str(readings))}

from typing import Any


def get_seasonal_context(location: str, plant: str | None = None) -> dict[str, Any]:
    return {
        "location": location,
        "seasonal_context": "Michigan gardeners should consider frost risk and indoor/outdoor transition timing.",
        "zone_note": "Zone 6a conditions can affect planting timing and watering needs.",
        "plant_context": f"Context prepared for {plant or 'general garden care'}.",
    }
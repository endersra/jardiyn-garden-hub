"""
JarDIYn tool registry for Project 3.

These are project-created tools exposed to Claude through the tools parameter.
Claude decides whether to call them. The backend executes the selected tool and
returns the result to Claude as a tool_result.
"""

from datetime import datetime
from typing import Any


JARDIYN_TOOLS = [
    {
        "name": "jardiyn_garden_memory_lookup",
        "description": "Look up saved garden context, plant focus, and care priorities for a user.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user profile identifier."
                },
                "plant": {
                    "type": "string",
                    "description": "The plant or garden topic the user is asking about."
                }
            },
            "required": ["user_id"]
        }
    },
    {
        "name": "jardiyn_seasonal_context",
        "description": "Return seasonal gardening context for a city, region, or month.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city or region for seasonal garden context."
                },
                "month": {
                    "type": "string",
                    "description": "The current or requested month."
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "jardiyn_watering_risk_check",
        "description": "Evaluate watering risk using soil condition, plant symptoms, humidity, and precipitation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "soil_status": {
                    "type": "string",
                    "description": "Observed soil condition, such as dry, damp, wet, or soggy."
                },
                "symptoms": {
                    "type": "string",
                    "description": "Observed plant symptoms, such as yellow leaves, curling, wilting, or brown spots."
                },
                "humidity_percent": {
                    "type": "number",
                    "description": "Current humidity percentage if available."
                },
                "precipitation_inches": {
                    "type": "number",
                    "description": "Recent or current precipitation in inches if available."
                }
            },
            "required": ["soil_status", "symptoms"]
        }
    }
]


def execute_jardiyn_tool(tool_name: str, tool_input: dict[str, Any]) -> str:
    """Execute one JarDIYn project-created tool selected by the model."""

    if tool_name == "jardiyn_garden_memory_lookup":
        user_id = tool_input.get("user_id", "public-frontend-user")
        plant = tool_input.get("plant", "general garden")

        return (
            f"Garden memory lookup for {user_id}: current plant focus is {plant}. "
            "Known beginner-care priorities are drainage, watering rhythm, light exposure, "
            "safe plant-care advice, and avoiding overconfident diagnosis."
        )

    if tool_name == "jardiyn_seasonal_context":
        city = tool_input.get("city", "Grand Rapids")
        month = tool_input.get("month") or datetime.utcnow().strftime("%B")

        return (
            f"Seasonal context for {city} in {month}: check current temperature, humidity, "
            "recent precipitation, frost risk, soil moisture, and local growing conditions "
            "before watering, planting, transplanting, or fertilizing."
        )

    if tool_name == "jardiyn_watering_risk_check":
        soil = str(tool_input.get("soil_status", "")).lower()
        symptoms = str(tool_input.get("symptoms", "")).lower()
        humidity = tool_input.get("humidity_percent")
        precipitation = tool_input.get("precipitation_inches")

        risk = "medium"
        recommendation = "Check the top inch of soil before watering."

        if "soggy" in soil or "wet" in soil or "yellow" in symptoms:
            risk = "high"
            recommendation = "Pause watering, check drainage, and let the top inch of soil dry before watering again."

        if isinstance(humidity, (int, float)) and humidity >= 75:
            recommendation += " High humidity may slow drying."

        if isinstance(precipitation, (int, float)) and precipitation > 0:
            recommendation += " Recent precipitation may reduce watering need."

        return f"Watering risk: {risk}. Recommendation: {recommendation}"

    return f"Unknown JarDIYn tool requested: {tool_name}"

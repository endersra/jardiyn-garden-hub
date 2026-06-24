import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.orchestrator import run_chat_workflow


app = FastAPI(
    title="JarDIYn Agent Backend",
    description="Phase 3 live agent runtime backend for JarDIYn by Garden Hub.",
    version="0.2.0",
)


DEFAULT_CORS_ORIGINS = (
    "http://127.0.0.1:5500,"
    "http://localhost:5500,"
    "https://endersra.github.io"
)

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGIN", DEFAULT_CORS_ORIGINS).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://endersra.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    user_id: str = "demo-user"


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "jardiyn-agent-backend",
        "phase": "phase-3-live-agent-runtime",
        "llm_mode": os.getenv("LLM_MODE", "mock").lower(),
    }


@app.post("/api/agent/chat")
def agent_chat(request: ChatRequest):
    return run_chat_workflow(
        user_message=request.message,
        user_id=request.user_id,
    )


WEATHER_CODE_LABELS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
}


def _weather_fallback(city: str, reason: str) -> dict:
    return {
        "location": {
            "name": city,
            "state": None,
            "country": None,
            "latitude": None,
            "longitude": None,
        },
        "current": {
            "temperature_f": None,
            "humidity_percent": None,
            "precipitation_inches": None,
            "wind_mph": None,
            "weather_code": None,
            "summary": "Weather temporarily unavailable",
        },
        "daily": {},
        "source": "weather_fallback",
        "warning": reason,
    }


@app.get("/api/weather")
def get_weather(city: str = "Grand Rapids"):
    """
    Real weather tool for Project 3 frontend.

    Uses Open-Meteo when available. If the external weather service fails,
    returns a safe fallback instead of breaking the frontend with a 502.
    """
    city = city.strip() or "Grand Rapids"

    headers = {
        "User-Agent": "JarDIYnGardenAssistant/1.0 educational project"
    }

    try:
        with httpx.Client(timeout=15.0, follow_redirects=True, headers=headers) as client:
            geo_response = client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={
                    "name": city,
                    "count": 1,
                    "language": "en",
                    "format": "json",
                },
            )

            if geo_response.status_code != 200:
                return _weather_fallback(
                    city,
                    f"Geocoding service returned status {geo_response.status_code}.",
                )

            geo_data = geo_response.json()
            results = geo_data.get("results") or []

            if not results:
                return _weather_fallback(city, f"No weather location found for {city}.")

            location = results[0]
            latitude = location["latitude"]
            longitude = location["longitude"]

            forecast_response = client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m",
                    "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
                    "forecast_days": 3,
                    "temperature_unit": "fahrenheit",
                    "wind_speed_unit": "mph",
                    "precipitation_unit": "inch",
                    "timezone": "auto",
                },
            )

            if forecast_response.status_code != 200:
                return _weather_fallback(
                    city,
                    f"Forecast service returned status {forecast_response.status_code}.",
                )

            forecast_data = forecast_response.json()

    except Exception as error:
        return _weather_fallback(city, f"Weather service unavailable: {error}")

    current = forecast_data.get("current", {})
    weather_code = current.get("weather_code")

    return {
        "location": {
            "name": location.get("name"),
            "state": location.get("admin1"),
            "country": location.get("country"),
            "latitude": latitude,
            "longitude": longitude,
        },
        "current": {
            "temperature_f": current.get("temperature_2m"),
            "humidity_percent": current.get("relative_humidity_2m"),
            "precipitation_inches": current.get("precipitation"),
            "wind_mph": current.get("wind_speed_10m"),
            "weather_code": weather_code,
            "summary": WEATHER_CODE_LABELS.get(weather_code, "Weather data available"),
        },
        "daily": forecast_data.get("daily", {}),
        "source": "open_meteo",
    }


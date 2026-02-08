from typing import Any
import logging
import httpx
from mcp.server.fastmcp import FastMCP

WEATHER_SERVICES_API_URL = "http://localhost:8000/weather_services"

mcp = FastMCP("fashion_server")


async def get_weather_data(self) -> Any:
    #TODO: update url and logic for API calls
    try:
        response = httpx.get(WEATHER_SERVICES_API_URL, headers={"Accept": "application/json"}, timeout=5.0)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        raise ValueError(f"Failed to retrieve weather data: {e}")


async def recommend_outfit(self, weather: str, occasion: str) -> str:
    #TODO: add a inference engine to recommend outfits based on weather conditions
    if weather == "sunny":
        return "I recommend wearing a light t-shirt and shorts."
    elif weather == "rainy":
        return "I recommend wearing a waterproof jacket and boots."
    elif weather == "cold":
        return "I recommend wearing a warm coat and scarf."
    else:
        return "I recommend dressing comfortably for the weather."

@mcp.tool()
async def get_outfit_suggestions(self, weather: str, occasion: str) -> Any:
    data = await self.recommend_outfit(weather=weather, occasion=occasion)
    if not data:
        raise ValueError("No outfit suggestions available")
    else:
        return {"outfit_suggestions": data}

@mcp.tool()
async def get_weather_info(self, location: str) -> Any:
    
    data = await self.get_weather_data()
    
    if not data:
        raise ValueError("No weather data available")
    
    for entry in data.get("weather", []):
        if entry.get("location") == location:
            return {
                "temperature": entry.get("temperature"),
                "condition": entry.get("condition")
            }
        else:
            raise ValueError(f"No weather information found for location: {location}")
    
    
def main():
    print("Starting fashion server!")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
    
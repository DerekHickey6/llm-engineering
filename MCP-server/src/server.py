from mcp.server.fastmcp import FastMCP
import requests
from langchain_community.tools import DuckDuckGoSearchRun

mcp = FastMCP("my-server")

@mcp.tool()
def search_web(query):
    """Searches web for query"""
    try:
        searcher = DuckDuckGoSearchRun()
        results = searcher.run(query)

        return results
    except Exception as e:
        return "Search Failed. Please try again"

@mcp.tool()
def get_weather(city):
    """Gets weather for a given city"""
    # Extract longitude and latitude
    geo_response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}")
    city_dict = geo_response.json()['results'][0]

    lat = city_dict['latitude']
    lon = city_dict['longitude']

    # Get weather data
    weather_response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true")

    current_weather_dict = weather_response.json()['current_weather']
    current_weather_units_dict = weather_response.json()['current_weather_units']
    time = f"{current_weather_dict['time'].split('T')[1]} {current_weather_dict['time'].split('T')[0]}"

    return f"""Weather for {city} at {time}

    Temperature: {current_weather_dict['temperature']} {current_weather_units_dict['temperature']}
    Windspeed:   {current_weather_dict['windspeed']} {current_weather_units_dict['windspeed']}
    Wind Direction: {current_weather_dict['winddirection']} {current_weather_units_dict['winddirection']}
    """



if __name__ == "__main__":
    print(get_weather("Nanaimo"))
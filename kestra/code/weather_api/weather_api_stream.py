import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from kestra import Kestra

def get_weather_data(is_historical: bool):
    """
    Fetch weather data from Open-Meteo API.
    
    :param is_historical: Flag to determine if data should be historical or current.
    :return: Processed weather data.
    """
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1 if is_historical else 3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://archive-api.open-meteo.com/v1/archive" if is_historical else "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": -10,
        "longitude": -55,
        "timezone": "America/Sao_Paulo"
    }
    
    if is_historical:
        params.update({
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "rain", "weather_code", "cloud_cover", "wind_direction_10m", "wind_speed_10m", "is_day"]
        })
    else:
        params.update({
            "hourly": "temperature_2m",
            "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "weather_code", "cloud_cover", "wind_direction_10m", "wind_speed_10m"]
        })
    
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
    
    if is_historical:
        hourly = response.Hourly()
        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )}
        
        for i, var in enumerate(params["hourly"]):
            hourly_data[var] = hourly.Variables(i).ValuesAsNumpy()
        
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        hourly_dataframe.to_csv("historical_data.csv", sep=";", index=False, encoding="utf-8")
        print(hourly_dataframe)
    else:
        current = response.Current()
        current_data = {var: current.Variables(i).Value() for i, var in enumerate(params["current"])}
        current_data["time"] = current.Time()

        print(current_data)
        
        return current_data
        
if __name__ == "__main__":
    output = get_weather_data(False)
    Kestra.outputs(output)

from datetime import date, time
from models.weater_forecast import WeatherForecast


class WeatherForecastHolder:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.__weather_forecastes: list[WeatherForecast] = []

    def get_all(self) -> list[WeatherForecast]:
        return self.__weather_forecastes

    def get_for_period(self, date_from: date, date_to: date) -> list[WeatherForecast] | None:
        weather_forecastes_for_period: list[WeatherForecast] = []
        for weather_forecast in self.__weather_forecastes:
            if date_from <= weather_forecast.date <= date_to:
                weather_forecastes_for_period.append(weather_forecast)
        return weather_forecastes_for_period if len(weather_forecastes_for_period) else None

    def add(self, date_forecast: date, time_forecast: time, temperature_c: int) -> WeatherForecast | None:
        for weather_forecast in self.__weather_forecastes:
            if weather_forecast.date == date_forecast and weather_forecast.time == time_forecast:
                return None
        new_weather_forecast = WeatherForecast(date=date_forecast,
                                               time=time_forecast,
                                               temperature_c=temperature_c,
                                               temperature_f=32 + int(temperature_c / 0.5556))
        self.__weather_forecastes.append(new_weather_forecast)
        return new_weather_forecast

    def update(self, date_forecast: date, time_forecast: time, new_temperature_c: int) -> WeatherForecast | None:
        for weather_forecast in self.__weather_forecastes:
            if weather_forecast.date == date_forecast and weather_forecast.time == time_forecast:
                weather_forecast.temperature_c = new_temperature_c
                weather_forecast.temperature_f = 32 + int(new_temperature_c / 0.5556)
                return weather_forecast
        return None

    def delete(self, date_forecast: date, time_forecast: time) -> bool:
        for weather_forecast in self.__weather_forecastes:
            if weather_forecast.date == date_forecast and weather_forecast.time == time_forecast:
                self.__weather_forecastes.remove(weather_forecast)
                return True
        return False

from pydantic import BaseModel
from datetime import date, time


class WeatherForecast(BaseModel):
    date: date
    time: time
    temperature_c: int
    temperature_f: int

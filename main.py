import uvicorn
import logging
from datetime import date, time
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from starlette import status
from starlette.responses import RedirectResponse
from models.weater_forecast import WeatherForecast
from models.weather_forecast_holder import WeatherForecastHolder


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI(openapi_url="/api/v1/openapi.json")
holder = WeatherForecastHolder()


def weather_forecast_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="WeatherForecastAPI",
        version="1.0.0",
        description="Учебный проект по созданию API для web-сервиса WeatherForecast (Прогноз погоды) с использованием "
                    "фреймворка FastAPI (Python)",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = weather_forecast_openapi


@app.get("/")
async def get_root():
    logger.info(f'Отработал GET запрос для отображения главного маршрута')
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


@app.get("/get-data/", response_model=list[WeatherForecast])
async def get_weather_forecastes():
    logger.info(f'Отработал GET запрос для отображения всех данных прогноза погоды')
    return holder.get_all()


@app.get("/get-data/{date_from}/{date_to}", response_model=list[WeatherForecast])
async def get_weather_forecast_for_period(date_from: date, date_to: date):
    sample = holder.get_for_period(date_from, date_to)
    if sample is not None:
        logger.info(f'Отработал GET запрос для отображения прогноза погоды за период с {date_from} по {date_to}.')
        return sample
    raise HTTPException(status_code=404, detail='За указанный период отсутствуют показатели')


@app.post("/add-data/{date_forecast}/{time_forecast}/{temperature}", response_model=WeatherForecast)
async def add_weather_forecast(date_forecast: date, time_forecast: time, temperature: int):
    new_data = holder.add(date_forecast, time_forecast, temperature)
    if new_data is not None:
        logger.info(f'Отработал POST запрос для добавления новых данных (дата: {date_forecast}, время: {time_forecast},'
                    f' температура: {temperature}).')
        return new_data
    raise HTTPException(status_code=500, detail='Прогноз погоды на указанную дату и время уже существует')


@app.put("/update-data/{date_forecast}/{time_forecast}/{new_temperature}", response_model=WeatherForecast)
async def update_weather_forecast(date_forecast: date, time_forecast: time, new_temperature: int):
    update_data = holder.update(date_forecast, time_forecast, new_temperature)
    if update_data is not None:
        logger.info(
            f'Отработал PUT запрос для обновления данных по дате {date_forecast}) и времени {time_forecast} '
            f'новым значением температуры {new_temperature}')
        return update_data
    raise HTTPException(status_code=404, detail='Прогноз погоды на указанную дату и время не найден')


@app.delete("/delete-data/{date_forecast}/{time_forecast}")
async def delete_weather_forecast(date_forecast: date, time_forecast: time):
    if holder.delete(date_forecast, time_forecast):
        logger.info(f'Отработал DELETE запрос для удаления данных по дате {date_forecast} и времени {time_forecast}.')
        return {'message': 'Прогноз погоды на указанную дату и время успешно удален'}
    raise HTTPException(status_code=404, detail='Прогноз погоды на указанную дату и время не найден')


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

from math import floor
from quart import Blueprint, jsonify, current_app
from http import HTTPStatus
from random import randrange

from weather.settings import CITY_IDS
from weather.collections.cities_weather import get_weather_data
from weather.tasks import collect_weather_data


weather_blueprint = Blueprint('weather', __name__)


@weather_blueprint.route("/<request_id>")
async def get_weather_status(request_id: str):
    weather_data = await get_weather_data(request_id)

    if not weather_data:
        return jsonify({"success": False}), HTTPStatus.NOT_FOUND

    collected_cities = len(weather_data['data'].keys())
    collected_cities_perc = floor(collected_cities * 100 / len(CITY_IDS))

    return jsonify(
        {
            'success': True,
            "request_id": request_id,
            "collected_cities": collected_cities,
            "collected_cities_%": collected_cities_perc,
            'collected_at': weather_data['timestamp'],
        }
    )


@weather_blueprint.route("/<request_id>/update")
async def update_weather_data(request_id: str):
    weather_data = await get_weather_data(request_id)

    if weather_data:                
        return jsonify({
            'success': False,
            'request_id': request_id
        }), HTTPStatus.CONFLICT
    
    current_app.add_background_task(collect_weather_data, request_id=request_id)
    
    return jsonify({
        'success': True,
        'request_id': request_id
    }), HTTPStatus.CREATED


@weather_blueprint.route("/openweather/<city_id>")
async def open_weather_mock(city_id: int):
    return jsonify(
        {
            "city_id": city_id,
            "humidity": randrange(5, 100),
            "temperature": randrange(5, 40),
        }
    )
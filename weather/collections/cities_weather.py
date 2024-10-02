from datetime import datetime
from weather.settings import CITIES_WEATHER_COLLECTION_NAME

from weather import database


async def set_weather_data(request_id: str, city_data: dict):
    try:
        document = {
            "temperature": city_data["temperature"],
            "humidity": city_data["humidity"],
            "timestamp": datetime.now(),
        }

        update_field = f'data.{city_data["city_id"]}'

        await database.get_collection(CITIES_WEATHER_COLLECTION_NAME).update_one(
            {"_id": request_id}, {"$set": {'timestamp': datetime.now(), update_field: document}}, upsert=True
        )
    except Exception as ex:
        print(ex)


async def get_weather_data(request_id: str):
    return await database.get_collection(CITIES_WEATHER_COLLECTION_NAME).find_one(
        {"_id": request_id}
    )


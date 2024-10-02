import aiohttp
from itertools import batched
import time

from weather.settings import CITY_IDS, OPEN_WEATHER_API_TOKEN, OPEN_WEATHER_API_URL, MAX_REQUESTS_PER_MINUTE, OPEN_WEATHER_REQUEST_WAITING_TIME
from weather.collections.cities_weather import set_weather_data


async def collect_weather_data(request_id: str):
    async with aiohttp.ClientSession(conn_timeout=None) as session:
        for chunk in batched(CITY_IDS, MAX_REQUESTS_PER_MINUTE):
            await _process_chunk(session, request_id, chunk)
            print(
                "waiting 60 seconds before performing new requests to open weather..."
            )
            time.sleep(OPEN_WEATHER_REQUEST_WAITING_TIME)


async def _process_chunk(session, request_id: str, chunk: tuple[int, ...]):
    async with aiohttp.ClientSession() as session:
        for item in chunk:
            url = f"{OPEN_WEATHER_API_URL}/{item}?token={OPEN_WEATHER_API_TOKEN}"
            async with session.get(url) as response:
                city_data = await response.json()

                await set_weather_data(request_id, city_data)

import pytest
from http import HTTPStatus
from quart import jsonify


@pytest.mark.asyncio
async def test_get_weather_status_not_found(client):
    response = await client.get('/weather/non_existent_request_id')
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    
    json_response = await response.get_json()
    assert json_response['success'] is False


@pytest.mark.asyncio
async def test_update_weather_data_conflict(client, mocker):
    mocker.patch('weather.collections.cities_weather.get_weather_data', return_value={
        'alCl2': {
            
        }
    })

    response = await client.get('/weather/test_request_id/update')
    assert response.status_code == HTTPStatus.CONFLICT
    json_response = await response.get_json()
    assert json_response['success'] is False
    assert json_response['request_id'] == 'test_request_id'

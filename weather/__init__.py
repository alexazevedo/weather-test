
from quart import Quart
from weather.blueprints import weather_blueprint


def create_app():
    app = Quart(__name__)
    app.register_blueprint(weather_blueprint, url_prefix='/weather')

    @app.route("/ping")
    async def ping() -> str:
        return ".. pong!"
    
    return app

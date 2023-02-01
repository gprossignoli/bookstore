import os

from flask import Flask
from config import Config


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)
	return app


if __name__ == '__main__':
	app = create_app()
	app.run(host=os.getenv("FLASK_RUN_PORT"), port=os.getenv("FLASK_RUN_PORT"))

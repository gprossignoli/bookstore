import os

from flask import Flask, g

from config.db import configure_db
from settings import SECRET_KEY


def create_app() -> Flask:
	app = Flask(__name__)
	app.config["SECRET_KEY"] = SECRET_KEY
	with app.app_context():
		configure_db(app)
		g.db.create_all()

	return app


if __name__ == '__main__':
	app = create_app()
	app.run(host=os.getenv("FLASK_RUN_PORT"), port=os.getenv("FLASK_RUN_PORT"))

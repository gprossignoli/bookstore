import os

from flask import Flask, g

from config.blueprints import register_blueprints
from config.db import configure_db
from settings import SECRET_KEY


def create_app() -> Flask:
	app = Flask(__name__)
	app.config["SECRET_KEY"] = SECRET_KEY
	with app.app_context():
		configure_db(app)
		g.db.create_all()
		register_blueprints(app)

	return app


if __name__ == '__main__':
	app = create_app()
	app.run(host="0.0.0.0", port=8002)

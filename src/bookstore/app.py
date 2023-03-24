from flask import Flask

from bookstore.config.blueprints import register_blueprints
from bookstore.config.db import configure_db
from bookstore.settings import SECRET_KEY, db


def create_app() -> Flask:
	app = Flask(__name__)
	app.config["SECRET_KEY"] = SECRET_KEY
	with app.app_context():
		configure_db(app, db)
		register_blueprints(app)

	return app


if __name__ == '__main__':
	app = create_app()
	app.run(host="0.0.0.0", port=8001)

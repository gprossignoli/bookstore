from flask import Flask

from api.book_routes import book_blueprint


def register_blueprints(app: Flask) -> None:
	app.register_blueprint(blueprint=book_blueprint)

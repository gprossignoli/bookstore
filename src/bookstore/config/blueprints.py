from flask import Flask

from bookstore.api.admin_routes import admin_blueprint
from bookstore.api.book_routes import book_blueprint
from bookstore.cli.kafka_load_tester import cli_commands


def register_blueprints(app: Flask) -> None:
	app.register_blueprint(blueprint=book_blueprint)
	app.register_blueprint(blueprint=admin_blueprint)
	app.register_blueprint(blueprint=cli_commands)

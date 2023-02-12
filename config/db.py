from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import DB_URI


def configure_db(app: Flask, db: SQLAlchemy) -> None:
	# create the extension
	# configure the SQLite database, relative to the app instance folder
	app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	# initialize the app with the extension
	db.init_app(app)
	db.create_all()

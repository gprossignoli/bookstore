import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	POSTGRES_USER = os.environ.get('DB_USERNAME')
	POSTGRES_PASSWORD = os.environ.get('DB_PASSWORD')
	POSTGRES_HOST = os.environ.get('DB_HOST')
	POSTGRES_PORT = os.environ.get('DB_PORT')
	POSTGRES_DB_NAME = os.environ.get('DB_NAME')
	SQLALCHEMY_DATABASE_URI = os.environ.get(f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

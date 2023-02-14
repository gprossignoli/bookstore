import csv
import re
from datetime import datetime
from typing import Dict, Union

import ujson
from cerberus import Validator
from cerberus.errors import ValidationError
from flask import Blueprint, Response, request
from flask_sqlalchemy.session import Session

from models.user import User
from src.models.book import Book
from settings import ROOT_DIR, db

admin_blueprint = Blueprint(name="admin", import_name=__name__, url_prefix="/admin")


@admin_blueprint.route("/gen_data", methods=["POST"])
def gen_data():
	file_path = f"{ROOT_DIR}/books.csv"

	with open(file_path, 'r') as file:
		reader = csv.DictReader(file)
		rows = [row for row in reader]
		rows = rows[:10000]

	session = Session(db)

	for row in rows:
		authors = row['authors']
		title = row['title']
		isbn = row['isbn']
		try:
			publication_date = datetime.strptime(row['publication_date'], '%m/%d/%Y').date()
		except Exception as e:
			print(e)
			continue

		publisher = row['publisher']
		book = Book(title=title, authors=authors, isbn=isbn, publication_date=publication_date, publisher=publisher)
		print(book.title, book.isbn)
		try:
			session.add(book)
			session.commit()
		except Exception as e:
			session.rollback()
			print(e)

	return Response(response={"Books inserted in DB"}, status=200)


@admin_blueprint.route("/create_user", methods=["POST"])
def create_user():
	data = __get_data_from_request()
	body = __validate_create_user_body(data)

	user = User(username=body["username"], first_name=body["first_name"], last_name=body["last_name"], email=body["email"])
	session = Session(db)
	try:
		session.add(user)
		session.commit()
	except Exception as e:
		session.rollback()
		raise e


def __get_data_from_request():
	data = request.data if len(request.data) > 0 else request.form
	try:
		data = ujson.loads(data)
	except TypeError as e:
		pass
	return data


def __validate_create_user_body(data: Dict) -> Union[Dict, Response]:
	schema = {
		"username": {
			"type": "string",
			"nullable": False,
			"empty": False,
		},
		"first_name": {
			"type": "string",
			"nullable": False,
			"empty": False,
		},
		"last_name": {
			"type": "string",
			"nullable": False,
			"empty": False,
		},
		"email": {
			"type": "string",
			"nullable": False,
			"empty": False,
			"check_with": __validate_email
		},
	}

	body = {"username": data.get("username"), "first_name": data.get("first_name"),
			"last_name": data.get("last_name"), "email": data.get("email")}
	try:
		v = Validator(schema=schema)
		v.allow_unknown = False
		val = v.validate(body, schema)

		if not val:
			return Response(response=f"Invalid request: {ujson.dumps(v.errors)}", status=400, mimetype='application/json')

		return v.normalized(body)

	except ValidationError as e:
		return Response(response=f"Invalid request: {e}", status=400, mimetype='application/json')


def __validate_email(field, value, error) -> None:
	regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
	if not re.fullmatch(regex, value):
		error(field, "User id has not a valid format")

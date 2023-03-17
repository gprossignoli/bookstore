import csv
import re
from datetime import datetime
from random import randint
from typing import Dict, Union

import ujson
from cerberus import Validator
from cerberus.errors import ValidationError
from flask import Blueprint, Response, request
from flask_sqlalchemy.session import Session

from bookstore.cli.kafka_load_tester import KafkaLoadTester
from bookstore.cli.report_generator import ReportGenerator
from bookstore.models.user import User
from bookstore.models.book import Book
from bookstore.settings import db, BOOKS_DATA_PATH

admin_blueprint = Blueprint(name="admin", import_name=__name__, url_prefix="/admin")


@admin_blueprint.route("/gen_data", methods=["POST"])
def gen_data():
	__generate_books_data()
	__generate_users_data()

	return Response(response={"Books and Users inserted in DB"}, status=200)


def __generate_books_data(session: Session = None) -> None:
	file_path = BOOKS_DATA_PATH
	with open(file_path, 'r') as file:
		reader = csv.DictReader(file)
		rows = [row for row in reader]
		rows = rows[:10000]

	if session is None:
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
		book = Book(title=title, authors=authors, isbn=isbn, publication_date=publication_date, publisher=publisher,
					stock=100000000, price=randint(10, 60))
		print(book.title, book.isbn)
		try:
			session.add(book)
			session.commit()
		except Exception as e:
			session.rollback()
			print(e)


def __generate_users_data(session: Session = None) -> None:
	users = [
		User(id="e5e61e0d-9bf9-4e54-9d1e-7d4b4af1e7a3", username="johndoe123", first_name="Emily",
			 last_name="Rodriguez", email="johnsmith@example.com", user_status=True),
		User(id="c3f4d9b9-037b-4b04-9e11-f2b37dc371a6", username="sarahsmith", first_name="Jacob", last_name="Kim",
			 email="jane.doe@gmail.com", user_status=True),
		User(id="a593c421-7147-4b88-a32f-af200109a1bc", username="brian.williams", first_name="Sophia",
			 last_name="Patel", email="mario.rossi@hotmail.com", user_status=True),
		User(id="4f80b2cf-cb4c-4a4a-b9c9-7e24b918c224", username="katie88", first_name="William", last_name="Chen",
			 email="amy.nguyen@yahoo.com", user_status=True),
		User(id="28d082e1-7ca7-4d72-b7e7-9c9b7f8256b9", username="markjones27", first_name="Natalie", last_name="Wong",
			 email="tom.baker@outlook.com", user_status=True),
	]

	if session is None:
		session = Session(db)

	for user in users:
		try:
			session.add(user)
			session.commit()
		except Exception as e:
			session.rollback()
			print(e)


@admin_blueprint.route("/gen_users_data", methods=["POST"])
def gen_users_data():
	__generate_users_data()
	return Response(response={"Users inserted in DB"}, status=200)


@admin_blueprint.route("/gen_books_data", methods=["POST"])
def gen_books_data():
	__generate_books_data()
	return Response(response={"Books and Users inserted in DB"}, status=200)


@admin_blueprint.route("/create_user", methods=["POST"])
def create_user():
	data = __get_data_from_request()
	body = __validate_create_user_body(data)

	user = User(username=body["username"], first_name=body["first_name"], last_name=body["last_name"],
				email=body["email"])
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
			return Response(response=f"Invalid request: {ujson.dumps(v.errors)}", status=400,
							mimetype='application/json')

		return v.normalized(body)

	except ValidationError as e:
		return Response(response=f"Invalid request: {e}", status=400, mimetype='application/json')


def __validate_email(field, value, error) -> None:
	regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
	if not re.fullmatch(regex, value):
		error(field, "User id has not a valid format")


@admin_blueprint.route("/load_test", methods=["POST"])
def load_test():
	KafkaLoadTester().execute()
	return Response(response={"load test completed"}, status=200)


@admin_blueprint.route("/generate_report", methods=["POST"])
def generate_report():
	ReportGenerator().generate_report()
	return Response(response={"report generation completed"}, status=200)


@admin_blueprint.route("/experiment", methods=["POST"])
def launch_experiment():
	iterations = int(request.args.get("iterations", 1))
	for i in range(iterations):
		KafkaLoadTester().execute()
		ReportGenerator().generate_report()
	return Response(response={f"Experiments completed: {iterations}"}, status=200)

from typing import Dict, Union
from uuid import UUID

import ujson
from flask import Blueprint, request, Response
from cerberus.validator import Validator
from cerberus.errors import ValidationError

from application.purchase_book.purchase_book_command import PurchaseBookCommand
from models.book_exception import BookException

book_blueprint = Blueprint(name="book", import_name=__name__, url_prefix="/books")


def __validate_user_id(field, value, error) -> None:
	try:
		UUID(value)
	except:
		error(field, "User id has not a valid format")


@book_blueprint.route("/<book_id>/purchase", methods=["POST"])
def purchase_book(book_id: int):
	data = __get_data_from_request()

	body = __validate_purchase_book_body(data)

	try:
		purchase_book_command = PurchaseBookCommand(book_id, body["user_id"], body["quantity"])
		purchase_book_command.execute()
		return Response(response=ujson.dumps("ok"), status=200, mimetype='application/json')
	except BookException as e:
		return Response(response=ujson.dumps(e.error), status=404, mimetype='application/json')


def __get_data_from_request():
	data = request.data if len(request.data) > 0 else request.form
	try:
		data = ujson.loads(data)
	except TypeError as e:
		pass
	return data


def __validate_purchase_book_body(data: Dict) -> Union[Dict, Response]:
	schema = {
		"user_id": {
			"type": "string",
			"nullable": False,
			"empty": False,
			"check_with": __validate_user_id
		},
		"quantity": {
			"type": "integer",
			"min": 1,
			"max": 1000,
			"nullable": False,
			"empty": False,
			"coerce": int,
		}
	}

	body = {"user_id": data.get("userId"), "quantity": data.get("quantity")}
	try:
		v = Validator(schema=schema)
		v.allow_unknown = False
		val = v.validate(body, schema)

		if not val:
			return Response(response=f"Invalid request: {ujson.dumps(v.errors)}", status=400, mimetype='application/json')

		return v.normalized(body)

	except ValidationError as e:
		return Response(response=f"Invalid request: {e}", status=400, mimetype='application/json')

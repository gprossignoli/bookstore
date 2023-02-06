from uuid import UUID

import ujson as ujson
from flask import Blueprint, request, Response
from cerberus.validator import Validator
from cerberus.errors import ValidationError

book_blueprint = Blueprint(name="book", import_name=__name__, url_prefix="/books")


def __validate_user_id(field, value, error) -> None:
	try:
		UUID(value)
	except:
		error(field, "User id has not a valid format")


@book_blueprint.route("/<book_id>/purchase", methods=["POST"])
def purchase_book(book_id: int):

	schema = {
		"userId": {
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

	data = request.data if len(request.data) > 0 else request.form
	try:
		data = ujson.loads(data)
	except TypeError as e:
		pass

	body = {"user_id": data.get("userId"), "quantity": data.get("quantity")}
	try:
		v = Validator(schema=schema)
		v.allow_unknown = True
		val = v.validate(body, schema)

		if not val:
			return Response(response=f"Invalid request: {ujson.dumps(v.errors)}", status=400,
							mimetype='application/json')

		body = v.normalized(body)

	except ValidationError as e:
		return Response(response=f"Invalid request: {e}", status=400,
						mimetype='application/json')

	try:
		purchase_book_command = PurchaseBookCommand()
		purchase_book_command.execute(book_id)

	except BookException as e:
		if e.error == 'User not found':
			return Response(response=ujson.dumps(e.error), status=404, mimetype='application/json')

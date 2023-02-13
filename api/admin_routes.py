import csv
import random
from datetime import datetime
from typing import List

from flask import Blueprint, Response
from flask_sqlalchemy.session import Session

from models.book import Book
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

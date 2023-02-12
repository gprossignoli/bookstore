import csv
import random
from datetime import datetime
from typing import List

from flask import Blueprint
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

	filtered_rows = __subset_rows_by_publisher(rows)

	session = Session(db)

	for row in filtered_rows:
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
		session.add(book)

	session.commit()


def __subset_rows_by_publisher(data) -> List:
	publishers = set([row['publisher'] for row in data])
	filtered_rows = []
	for publisher in publishers:
		publisher_rows = [row for row in data if row['publisher'] == publisher]
		filtered_row = random.choice(publisher_rows)
		filtered_rows.append(filtered_row)

	return random.sample(filtered_rows, min(len(filtered_rows), 10000))

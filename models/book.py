from flask import g

db = g.get("db")


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    isbn = db.Column(db.String, unique=True, nullable=False)

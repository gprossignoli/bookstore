from settings import db


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    isbn = db.Column(db.String, unique=True, nullable=False)
    authors = db.Column(db.String, nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    publisher = db.Column(db.String, unique=True, nullable=False)
    stock = db.Column(db.Integer, default=100000000, nullable=False)
    purchases = db.relationship('Purchase', backref='books')

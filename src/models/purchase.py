from settings import db


class Purchase(db.Model):
	__tablename__ = "purchases"
	id = db.Column(db.Integer, primary_key=True)
	book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
	user_id = db.Column(db.String, db.ForeignKey('user.id'))
	quantity_id = db.Column(db.Integer)

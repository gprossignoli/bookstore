class BookException(Exception):
	def __init__(self, message: str):
		self.error = message

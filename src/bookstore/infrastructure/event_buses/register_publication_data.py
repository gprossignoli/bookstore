import functools
from datetime import datetime

from bookstore.settings import publication_data_logger


def register_publication_data(function):
	@functools.wraps(function)
	def wrapper(*args, **kwargs):
		timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
		publication_data_logger.info(f"Event:{kwargs['event'].id},published_at:{timestamp}")
		try:
			function(*args, **kwargs)
		except Exception as e:
			publication_data_logger.info(
				f"Event:{kwargs['event'].id},failed_to_publish_at:{timestamp}")
			raise e

	return wrapper

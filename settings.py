import os
import logging
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv


ROOT_DIR = os.path.dirname((os.path.realpath(__file__)))
ENV_FILE = os.path.abspath(os.path.join(ROOT_DIR, ".env"))

load_dotenv(ENV_FILE)

# LOGGING CONFIG

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('bookstore')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# to log debug messages
debug_logger = logging.StreamHandler()
debug_logger.setLevel(logging.DEBUG)
debug_logger.setFormatter(formatter)

# to log general messages
# x2 files of 2mb
info_logger = RotatingFileHandler(filename='bookstore.log', maxBytes=2097152, backupCount=2)
info_logger.setLevel(logging.INFO)
info_logger.setFormatter(formatter)

# to log errors messages
error_logger = RotatingFileHandler(filename='bookstore_errors.log', maxBytes=2097152, backupCount=2)
error_logger.setLevel(logging.ERROR)
error_logger.setFormatter(formatter)

logger.addHandler(debug_logger)
logger.addHandler(info_logger)
logger.addHandler(error_logger)

# API
SECRET_KEY = os.getenv("SECRET_KEY")

# database connection
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

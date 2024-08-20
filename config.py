import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)


FAST_API_ORIGIN = os.getenv('FAST_API_ORIGIN')
REACT_ORIGIN = os.getenv('REACT_ORIGIN')



import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


FAST_API_ORIGIN = os.getenv('FAST_API_ORIGIN')
REACT_ORIGIN = os.getenv('REACT_ORIGIN')



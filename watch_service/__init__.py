from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

import config

engine: Engine = None
if config.SQLALCHEMY_DATABASE_URI is not None:
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

from app.database.base import Base
from app.database.session import engine

import app.models


def create_tables():
    Base.metadata.create_all(bind=engine)
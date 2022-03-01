from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import DATE, CHAR, INTEGER

from ._base import Base

class books(Base):
    __tablename__ = 'books'
    id = Column(INTEGER(), primary_key=True)
    title = Column(CHAR(256))


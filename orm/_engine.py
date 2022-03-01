from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData

engine = create_engine('sqlite:///{}'.format('/home/database/oscar.sqlite3'))
# engine = create_engine('sqlite:///C:/Users/jake/oscar.sqlite3')
metadata = MetaData(bind=engine)
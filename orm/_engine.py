from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData

engine = create_engine('sqlite:///{}'.format('/home/database/oscar.sqlite3'))
# engine = create_engine('sqlite:///C:/Users/jake/oscar.sqlite3',
#                         connect_args={'check_same_thread': False})
metadata = MetaData(bind=engine)
from contextlib import ContextDecorator
from sqlalchemy.orm.session import Session as ORM_Session
from werkzeug.local import LocalProxy
from ._engine import engine

class Session (ContextDecorator):
    _session_instance = None
    _reentrant_count = 0

    def __init__ (self, _rollback_on_error=True):
        self._rollback_on_error = _rollback_on_error

    def __enter__ (self):
        if Session._reentrant_count == 0:
            Session._session_instance = ORM_Session(bind=engine)
        Session._reentrant_count += 1
        return Session._session_instance

    def __exit__ (self, exc_type, exc_val, exc_tb): 
        Session._reentrant_count -= 1
        if exc_type is None and exc_val is None and exc_tb is None:
            if Session._reentrant_count == 0:
                Session._session_instance.commit()
        elif self._rollback_on_error:
            Session._session_instance.rollback()
        if Session._reentrant_count == 0:
            Session._session_instance.close()
            Session._session_instance = None
            from ._base import Base
            Base._flush_cache()

    @staticmethod
    def _get_session_instance():
        if Session._session_instance is None:
            raise RuntimeError('Session not init')
        return Session._session_instance

session = LocalProxy(Session._get_session_instance)

@Session()
def query(sql):
    conn = session.connection().engine.raw_connection()
    # c = conn.cursor(as_dict=True)
    c = conn.cursor()
    c.execute(sql)
    return c.fetchall()

@Session()
def postUser(user, year, win, fav):
    conn = session.connection().engine.raw_connection()
    c = conn.cursor()
    for cat in win.keys():
        if cat in win and cat in fav:
            c.execute('INSERT INTO oscar_users (User, Year, Cat, Won, Favorite) VALUES (?, ?, ?, ?, ?)', 
            (user, year, cat, win[cat], fav[cat]))
        else: 
            if cat in win:
                c.execute('INSERT INTO oscar_users (User, Year, Cat, Won, Favorite) VALUES (?, ?, ?, ?, ?)', 
                (user, year, cat, win[cat], ''))
            elif cat in fav:
                c.execute('INSERT INTO oscar_users (User, Year, Cat, Won, Favorite) VALUES (?, ?, ?, ?, ?)', 
                (user, year, cat, '', fav[cat]))
    conn.commit()
    # conn.close()
    return 'posted'

@Session()
def postWinners(year, cat):
    conn = session.connection().engine.raw_connection()
    c = conn.cursor()
    for ca in cat:
        c.execute('INSERT INTO oscar_winners (Cat, Year, Name, Weight) VALUES (?, ?, ?, ?)', 
        (ca, year, '', 1))
    conn.commit()
    # conn.close()
    return 'posted'




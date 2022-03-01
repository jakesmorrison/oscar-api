from sqlalchemy.ext.declarative import declarative_base
from ._engine import metadata
from ._session import session
import collections

class MyBase:
    def __str__(self):
        return self

    _name_cache = collections.defaultdict(dict)
        
    @staticmethod
    def _flush_cache():
        MyBase._name_cache = collections.defaultdict(dict)

Base = declarative_base(cls=MyBase, metadata=metadata)
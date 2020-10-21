from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from database import db


class Track(db.Model):
    __tablename__ = 'track'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    location = Column(String(128))
    size = Column(String(128))
    user_id = Column(Integer, ForeignKey('user.id'))

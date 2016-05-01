from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from collections import OrderedDict
from datetime import datetime

from pbtaskrunner.database import Base


class DictSerializable(object):
    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result


class TestTask(Base, DictSerializable):
    """Database representation of a Task test"""
    __tablename__ = 'test_task'
    request_id = Column(Integer, primary_key=True)
    requester = Column('requester', String(30))
    created = Column(DateTime, default=datetime.now)
    test_environment = Column('test_environment', Integer)
    template = Column('template', String(256))
    status = Column('status', String(15))
    output = Column('output', Text)
    task_id = Column('task_id', String(40))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TestEnvironment(Base, DictSerializable):
    """Database representation of a test environment"""
    __tablename__ = 'test_environment'
    id = Column(Integer, primary_key=True)
    env_number = Column(Integer)
    in_use = Column(Boolean, default=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

from pbtaskrunner import db
from pbtaskrunner import app

from datetime import datetime


def date_time_now():
    return datetime.now


class TestTask(db.Model):
    """Database representation of a Task test"""
    __tablename__ = 'test_task'
    request_id = db.Column(db.Integer, primary_key=True)
    requester = db.Column('requester', db.String(30))
    created = db.Column(db.DateTime, default=date_time_now())
    test_environment = db.Column('test_environment', db.Integer)
    template = db.Column('template', db.String(256))
    status = db.Column('status', db.String(15))
    output = db.Column('output', db.Text)
    task_id = db.Column('task_id', db.String(40))


class TestEnvironment(db.Model):
    """Database representation of a test environment"""
    __tablename__ = 'test_environment'
    id = db.Column(db.Integer, primary_key=True)
    env_number = db.Column(db.Integer)
    in_use = db.Column(db.Boolean, default=False)

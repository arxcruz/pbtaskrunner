from pbtaskrunner import db
from pbtaskrunner.models import TestEnvironment


def create_database():
    db.create_all()


def load_environments():
    for x in range(1, 101):
        test = TestEnvironment(env_number=x, in_use=False)
        db.session.add(test)
    db.session.commit()

if __name__ == '__main__':
    create_database()
    load_environments()

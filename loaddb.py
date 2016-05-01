from pbtaskrunner.database import db_session
from pbtaskrunner.database import init_db
from pbtaskrunner.models import TestEnvironment


def load_environments():
    init_db()

    for x in range(1, 101):
        test = TestEnvironment()
        test.env_number = x
        test.in_use = False
        db_session.add(test)
    db_session.commit()

if __name__ == '__main__':
    load_environments()

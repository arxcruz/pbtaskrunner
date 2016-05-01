from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pbtaskrunner import app

engine = create_engine(app.config['DATABASE_URI'],
                       convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


def init_db(args=None):
    Base.metadata.create_all(bind=engine)

Base = declarative_base(name='Base')
Base.query = db_session.query_property()

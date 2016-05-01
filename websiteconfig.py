import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE_URI = 'sqlite:///%s' % os.path.join(_basedir, 'pbtaskrunner.db')
DATABASE_CONNECT_OPTIONS = {}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

TESTS_DIR = "/home/arxcruz/ansible"
SCRIPT_FILE = "/media/psf/pbtaskrunner/scripts/run_test.sh"

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 5000

SECRET_KEY = 'herpaderp'

SOURCE_ROOT = '%s' % os.path.join(_basedir, 'local')

del os

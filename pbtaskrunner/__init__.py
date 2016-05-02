from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse
from flask_restful import Api
from flask_restful import Resource

from celery import Celery
import random
import re
import subprocess
import time
import unittest
import json


__version__ = '0.1'

# Initialize Flask
app = Flask(__name__)
app.config.from_object('websiteconfig')
app.secret_key = 'a6ac0d63-abbc-4bb4-9702-8408392f9dff'

# Initialize database
db = SQLAlchemy(app)

# Initialize flask-restful
api = Api(app)

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Test Task REST Api
test_fields = {
    'request_id': fields.Integer,
    'requester': fields.String,
    'created': fields.DateTime(dt_format='iso8601'),
    'test_environment': fields.Integer,
    'template': fields.String,
    'status': fields.String,
    'output': fields.String,
    'task_id': fields.String,
    'uri': fields.Url('testtask', absolute=True)
}

test_parser = reqparse.RequestParser()
test_parser.add_argument('requester')
test_parser.add_argument('test_environment')
test_parser.add_argument('template')
test_parser.add_argument('status')
test_parser.add_argument('output')
test_parser.add_argument('task_id')


class TestTaskResource(Resource):
    # @marshal_with(test_fields)
    def get(self, request_id):
        test = TestTask.query.get(request_id)
        if test:
            if test.status not in ['IN PROGRESS', 'PENDING']:
                # We already have all the output
                return {'output': test.output, 'status': test.status}
            task = run_tests.AsyncResult(test.task_id)
            return {'output': task.info.get('output'), 'status': 'IN PROGRESS'}
        abort(404, message='Test doesn\'t exist')

    @marshal_with(test_fields)
    def put(self, request_id):
        test = TestTask.query.get(request_id)
        if not test:
            abort(404)

        args = test_parser.parse_args()
        test.output = args['output']
        test.requester = args['requester']
        test.test_environment = args['test_environment']
        test.template = args['template']
        test.status = args['status']

        db.session.commit()
        return test, 201


class TestTaskListResource(Resource):
    @marshal_with(test_fields)
    def get(self):
        tests = TestTask.query.all()
        return tests

    @marshal_with(test_fields)
    def post(self):
        args = test_parser.parse_args()
        test_environment = args['test_environment']
        env = TestEnvironment.query.get(test_environment)
        if not env:
            abort(404, 'Test environment not found')

        if env.in_use:
            error_message = ('You cannot use a test environment that\'s'
                             'already in use')
            abort(404, message=error_message)

        test = TestTask()
        test.requester = args['requester']
        test.test_environment = args['test_environment']
        test.template = args['template']
        test.status = 'PENDING'

        db.session.add(test)
        env.in_use = True
        db.session.commit()
        task = run_tests.apply_async(args=[test.request_id])
        test.task_id = task.id
        db.session.commit()

        return test, 201


test_env_fields = {
    'id': fields.Integer,
    'env_number': fields.Integer,
    'in_use': fields.Boolean
}


class TestEnvironmentListResource(Resource):
    @marshal_with(test_env_fields)
    def get(self):
        test_envs = TestEnvironment.query.all()
        return test_envs


api.add_resource(TestTaskResource, '/api/v1.0/testtask/<int:request_id>',
                 endpoint='testtask')
api.add_resource(TestTaskListResource, '/api/v1.0/testtask',
                 endpoint='testtasks')
api.add_resource(TestEnvironmentListResource, '/api/v1.0/envs',
                 endpoint='envs')

# End Test Task REST Api


@app.teardown_request
def remove_db_session(exception):
    db.session.remove()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE')
    return response


@app.route('/api/v1.0/tests')
def get_tests():
    loader = unittest.TestLoader()
    discovered_tests = loader.discover(app.config['TESTS_DIR'])
    tests = discovered_tests._tests
    regex_exp = 'testMethod=(.*?)\>]>'
    return_value = [re.search(regex_exp, str(t)).group(1) for t in tests]
    return json.dumps({'tests': return_value})


@celery.task(bind=True)
def run_tests(self, test_id):
    """Background task that runs a long function with progress reports."""
    test = TestTask.query.get(test_id)
    if not test:
        return {}

    result = ''
    args = ['/bin/bash', app.config['SCRIPT_FILE'], app.config['TESTS_DIR'],
            test.template]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         bufsize=1)
    test.status = 'IN PROGRESS'
    db.session.commit()

    for line in iter(p.stdout.readline, b''):
        result += line + '\n'
        self.update_state(state='IN PROGRESS', meta={'output': result})

    for line in iter(p.stderr.readline, b''):
        result += line + '\n'

    p.stdout.close()
    return_value = p.wait()
    result += 'Returned value: %s' % return_value
    self.update_state(state='COMPLETE', meta={'output': result})

    if return_value == 0:
        test.status = 'COMPLETE'
    else:
        test.status = 'ERROR'

    test.output = result
    env = TestEnvironment.query.get(test.test_environment)
    if env:
        env.in_use = False

    db.session.commit()
    return {'output': result, 'return_value': return_value}

    # verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    # adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    # noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    # message = ''
    # total = random.randint(10, 50)
    # test = TestTask.query.get(test_id)
    # if not test:
    #     return {}
    #
    # for i in range(total):
    #     if not message or random.random() < 0.25:
    #         message = '{0} {1} {2}...'.format(random.choice(verb),
    #                                           random.choice(adjective),
    #                                           random.choice(noun))
    #     test.status = 'IN PROGRESS'
    #     test.output = message
    #     self.update_state(state='PROGRESS',
    #                       meta={'current': i, 'total': total,
    #                             'output': message})
    #     db_session.commit()
    #     time.sleep(1)
    #
    # test.status = 'COMPLETE'
    # env = TestEnvironment.query.get(test.test_environment)
    # if env:
    #     env.in_use = False
    # db_session.commit()
    #
    # return {'current': 100, 'total': 100, 'output': 'Task completed!',
    #         'result': 42}


from pbtaskrunner.models import TestTask, TestEnvironment

import os
import tempfile
import unittest
import datetime

import json
import mock

from pbtaskrunner import run_tests
from pbtaskrunner import app, db
from pbtaskrunner.models import TestEnvironment
from pbtaskrunner.models import TestTask


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_file = tempfile.mkstemp()
        uri = 'sqlite:///%s' % str(self.db_file)
        app.config['SQLALCHEMY_DATABASE_URI'] = uri
        app.config['TESTING'] = True
        app.config['CELERY_ALWAYS_EAGER'] = True
        self.app = app.test_client()
        db.create_all()
        self._load_env_database()
        self._load_test_task_database()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.close(self.db_fd)
        os.unlink(self.db_file)

    def _load_env_database(self):
        test = TestEnvironment(env_number=1, in_use=False)
        db.session.add(test)
        test = TestEnvironment(env_number=2, in_use=True)
        db.session.add(test)
        db.session.commit()

    def _load_test_task_database(self):
        task = TestTask(requester='Dummy1', test_environment=1,
                        template='tests.test_get_tasks1', status='COMPLETE',
                        output='Test finished', task_id='dummy-id-1',
                        created=datetime.datetime(2016, 05, 01))
        db.session.add(task)
        task = TestTask(requester='Dummy2', test_environment=2,
                        template='tests.test_get_tasks2', status='ERROR',
                        output='Test fails', task_id='dummy-id-2',
                        created=datetime.datetime(2016, 05, 01))
        db.session.add(task)
        task = TestTask(requester='Dummy3', test_environment=3,
                        template='tests.test_get_tasks3', status='IN PROGRESS',
                        output='Test in progress', task_id='dummy-id-3',
                        created=datetime.datetime(2016, 05, 01))
        db.session.add(task)
        task = TestTask(requester='Dummy4', test_environment=4,
                        template='tests.test_get_tasks4', status='PENDING',
                        output='Test pending', task_id='dummy-id-4',
                        created=datetime.datetime(2016, 05, 01))
        db.session.add(task)
        db.session.commit()

    def test_get_env(self):
        response = self.app.get('/api/v1.0/envs')
        envs = load_json(response)
        self.assertEqual([{'env_number': 1, 'id': 1, 'in_use': False},
                          {'env_number': 2, 'id': 2, 'in_use': True}],
                         envs)

    def test_get_tasks(self):
        response = self.app.get('/api/v1.0/testtask')
        tasks = load_json(response)
        expected = [{u'status': u'COMPLETE', u'test_environment': 1,
                     u'task_id': u'dummy-id-1',
                     u'created': u'2016-05-01T00:00:00',
                     u'requester': u'Dummy1',
                     u'uri': u'http://localhost/api/v1.0/testtask/1',
                     u'template': u'tests.test_get_tasks1', u'request_id': 1,
                     u'output': u'Test finished'},
                    {u'status': u'ERROR', u'test_environment': 2,
                     u'task_id': u'dummy-id-2',
                     u'created': u'2016-05-01T00:00:00',
                     u'requester': u'Dummy2',
                     u'uri': u'http://localhost/api/v1.0/testtask/2',
                     u'template': u'tests.test_get_tasks2', u'request_id': 2,
                     u'output': u'Test fails'},
                    {u'status': u'IN PROGRESS', u'test_environment': 3,
                     u'task_id': u'dummy-id-3',
                     u'created': u'2016-05-01T00:00:00',
                     u'requester': u'Dummy3',
                     u'uri': u'http://localhost/api/v1.0/testtask/3',
                     u'template': u'tests.test_get_tasks3', u'request_id': 3,
                     u'output': u'Test in progress'},
                    {u'status': u'PENDING', u'test_environment': 4,
                     u'task_id': u'dummy-id-4',
                     u'created': u'2016-05-01T00:00:00',
                     u'requester': u'Dummy4',
                     u'uri': u'http://localhost/api/v1.0/testtask/4',
                     u'template': u'tests.test_get_tasks4', u'request_id': 4,
                     u'output': u'Test pending'}]
        self.assertEqual(expected, tasks)

    @mock.patch('pbtaskrunner.run_tests.AsyncResult')
    def test_get_task_by_id(self, run_tests_mock):
        run_tests_mock.return_value.info.get.return_value = 'Test in progress'

        # Get the output from the database for  dummy test 1
        response = self.app.get('/api/v1.0/testtask/1')
        task = load_json(response)
        self.assertEqual({'status': 'COMPLETE',
                          'output': 'Test finished'}, task)

        # Get the output from the celery worker from dummy test 2
        # Since it's still in progress
        response = self.app.get('/api/v1.0/testtask/3')
        task = load_json(response)
        run_tests_mock.assert_called_once_with('dummy-id-3')
        self.assertEqual({'output': 'Test in progress',
                          'status': 'IN PROGRESS'}, task)

    @mock.patch('pbtaskrunner.run_tests.apply_async')
    def test_post_task(self, run_tests_mock):
        # Post a task in an in use environment
        data = {'requester': 'Dummy requester', 'test_environment': 2,
                'template': 'test_dummy_task', 'status': 'PENDING'}
        response = self.app.post('/api/v1.0/testtask', data=data)
        self.assertEqual(404, response.status_code)

        # Post a task in a not used environment
        data = {'requester': 'Dummy requester', 'test_environment': 1,
                'template': 'test_dummy_task', 'status': 'PENDING'}

        run_tests_mock.return_value.id = 'dummy-id-5'
        response = self.app.post('/api/v1.0/testtask', data=data)
        task = load_json(response)
        # Because I have no idea how to mock the datetime and I want to keep
        # it simple
        del task['created']
        expected = {'status': 'PENDING', 'test_environment': 1,
                    'task_id': 'dummy-id-5', 'template': 'test_dummy_task',
                    'request_id': 5, 'output': None,
                    'requester': 'Dummy requester',
                    'uri': 'http://localhost/api/v1.0/testtask/5'}
        self.assertEqual(expected, task)
        run_tests_mock.assert_called_once()


def load_json(api_response):
    return json.loads(api_response.data.decode('utf8'))

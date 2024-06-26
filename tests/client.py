"""
Tests for clients that connect to the BigBoat API.

Copyright 2017-2020 ICTU
Copyright 2017-2022 Leiden University
Copyright 2017-2024 Leon Helwerda

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
import unittest
import requests
import requests_mock
from requests_mock.request import _RequestObjectProxy as Request
from requests_mock.response import _Context as Context
import yaml
from bigboat.client import Client, Client_v1, Client_v2

class Client_Test(unittest.TestCase):
    """
    Tests for the generic client base class.
    """

    URL = 'http://dashboard.example/'
    CANONICAL_URL = 'http://dashboard.example'

    def setUp(self) -> None:
        super().setUp()
        self.client = Client(self.URL)

    def test_base_url(self) -> None:
        """
        Test the Client.base_url property.
        """

        # The base_url should return an URL without trailing slash.
        self.assertEqual(self.client.base_url, self.CANONICAL_URL)

    def test_interface(self) -> None:
        """
        Test whether the abstract base class requires the minimal interface.
        """

        with self.assertRaises(NotImplementedError):
            self.client.apps()
        with self.assertRaises(NotImplementedError):
            self.client.get_app('foo', 'latest')
        with self.assertRaises(NotImplementedError):
            self.client.update_app('foo', 'latest')
        with self.assertRaises(NotImplementedError):
            self.client.delete_app('foo', 'latest')
        with self.assertRaises(NotImplementedError):
            self.client.instances()
        with self.assertRaises(NotImplementedError):
            self.client.get_instance('bar')
        with self.assertRaises(NotImplementedError):
            self.client.update_instance('bar', 'foo', 'latest',
                                        extra={'ignored': 'yes'})
        with self.assertRaises(NotImplementedError):
            self.client.delete_instance('bar')

class RequestsTestCase(unittest.TestCase):
    """
    A base unit test class that uses requests.

    This class provides a requests_mock member variable during the test run.
    """

    def setUp(self) -> None:
        super().setUp()
        self.requests_mock = requests_mock.mock(case_sensitive=True)
        self.requests_mock.start()

    def tearDown(self) -> None:
        super().tearDown()
        self.requests_mock.stop()

class Client_v1_Test(RequestsTestCase):
    """
    Tests for the BigBoat v1 API.
    """

    URL = 'http://dashboard.example/'
    PATH = 'api/v1/'

    def setUp(self) -> None:
        super().setUp()
        self.client = Client_v1(self.URL)

    def test_apps(self) -> None:
        """
        Test the Client_v1.apps dummy method.
        """

        self.assertEqual(self.client.apps(), [])

    def test_get_app(self) -> None:
        """
        Test the Client_v1.get_app method.
        """

        self.requests_mock.get(f'{self.URL}{self.PATH}appdef/foo/latest',
                               text='''name: foo
version: latest
instance:
  image: hello-world
''')
        application = self.client.get_app('foo', 'latest')
        assert application is not None
        self.assertEqual(application.name, 'foo')
        self.assertEqual(application.version, 'latest')

        # Test connection error for nonexistent applications.
        self.requests_mock.get(f'{self.URL}{self.PATH}appdef/does/notexist',
                               exc=requests.exceptions.ConnectionError)
        self.assertIsNone(self.client.get_app('does', 'notexist'))

    def test_update_app(self) -> None:
        """
        Test the Client_v1.update_app dummy method.
        """

        self.assertIsNone(self.client.update_app('foo', 'latest'))

    def test_delete_app(self) -> None:
        """
        Test the Client_v1.delete_app method.
        """

        self.requests_mock.delete(f'{self.URL}{self.PATH}appdef/foo/latest')
        self.requests_mock.delete(f'{self.URL}{self.PATH}appdef/does/notexist',
                                  status_code=404)

        self.assertTrue(self.client.delete_app('foo', 'latest'))
        self.assertFalse(self.client.delete_app('does', 'notexist'))

    def test_instances(self) -> None:
        """
        Test the Client_v1.instances method.
        """

        self.requests_mock.get(f'{self.URL}{self.PATH}instances',
                               status_code=404)
        self.assertEqual(self.client.instances(), [])

        self.requests_mock.get(f'{self.URL}{self.PATH}instances',
                               json={
                                   "statusCode": 200,
                                   "instances": ['foo', 'bar', 'baz']
                               })
        instances = self.client.instances()
        names = list(sorted(instance.name for instance in instances))
        self.assertEqual(names, ['bar', 'baz', 'foo'])

    def test_get_instance(self) -> None:
        """
        Test the Client_v1.get_instance method.
        """

        self.requests_mock.get(f'{self.URL}{self.PATH}state/qux',
                               status_code=404)
        self.requests_mock.get(f'{self.URL}{self.PATH}state/foo',
                               text='active')

        self.assertIsNone(self.client.get_instance('qux'))
        instance = self.client.get_instance('foo')
        assert instance is not None
        self.assertEqual(instance.name, 'foo')
        self.assertEqual(instance.current_state, 'running')

    def test_update_instance(self) -> None:
        """
        Test the update_instance method.
        """

        url = f'{self.URL}{self.PATH}'
        self.requests_mock.get(f'{url}start-app/does/notexist/qux',
                               status_code=404)
        self.requests_mock.get(f'{url}start-app/foo/latest/foo')

        self.assertIsNone(self.client.update_instance('qux', 'does', 'notexist',
                                                      more={'random': 'args'}))
        instance = self.client.update_instance('foo', 'foo', 'latest')
        assert instance is not None
        self.assertEqual(instance.name, 'foo')
        self.assertEqual(instance.current_state, 'running')
        self.assertEqual(instance.application.name, 'foo')
        self.assertEqual(instance.application.version, 'latest')

    def test_delete_instance(self) -> None:
        """
        Test the Client_v1.delete_instance method.
        """

        self.requests_mock.get(f'{self.URL}{self.PATH}stop-app/qux',
                               status_code=404)
        self.requests_mock.get(f'{self.URL}{self.PATH}stop-app/foo')

        self.assertIsNone(self.client.delete_instance('qux'))
        instance = self.client.delete_instance('foo')
        assert instance is not None
        self.assertEqual(instance.name, 'foo')
        self.assertEqual(instance.current_state, 'created')

class Client_v2_Test(RequestsTestCase):
    """
    Tests for the BigBoat v2 API.
    """

    URL = 'http://dashboard.example/'
    PATH = 'api/v2/'
    KEY = 'my-api-key'

    def setUp(self) -> None:
        super().setUp()
        self.client = Client_v2(self.URL, self.KEY)

    def test_apps(self) -> None:
        """
        Test the Client_v2.apps method.
        """

        self.requests_mock.get(f'{self.URL}{self.PATH}apps',
                               json=[
                                   {
                                       "id": "ERfrBncoPKSN9ampt",
                                       "name": "nginx",
                                       "version": "latest"
                                   },
                                   {
                                       "id": "LENn6QcjnG8WRvAxf",
                                       "name": "nginx",
                                       "version": "1.11.4"
                                   }
                               ])

        apps = self.client.apps()
        app_pairs = list(sorted((app.name, app.version) for app in apps))
        self.assertEqual(app_pairs, [('nginx', '1.11.4'), ('nginx', 'latest')])

    def test_get_app(self) -> None:
        """
        Test the Client_v2.get_app method.
        """

        self.requests_mock.get(f'{self.URL}{self.PATH}apps/does/notexist',
                               status_code=404)
        self.requests_mock.get(f'{self.URL}{self.PATH}apps/nginx/latest',
                               json={
                                   "id": "MKMZCnLcEJmkjSenJ",
                                   "name": "nginx",
                                   "version": "latest"
                               })

        self.assertIsNone(self.client.get_app('does', 'notexist'))

        app = self.client.get_app('nginx', 'latest')
        assert app is not None
        self.assertEqual(app.name, 'nginx')
        self.assertEqual(app.version, 'latest')

    def test_update_app(self) -> None:
        """
        Test the Client_v2.update_app method.
        """

        self.requests_mock.put(f'{self.URL}{self.PATH}apps/%3Cfoo%3E/0',
                               exc=requests.exceptions.ConnectionError)
        self.requests_mock.put(f'{self.URL}{self.PATH}apps/nginx/latest',
                               status_code=201,
                               json={
                                   "id": "MKMZCnLcEJmkjSenJ",
                                   "name": "nginx",
                                   "version": "latest"
                               })

        self.assertIsNone(self.client.update_app('<foo>', '0'))
        app = self.client.update_app('nginx', 'latest')
        assert app is not None
        self.assertEqual(app.name, 'nginx')
        self.assertEqual(app.version, 'latest')

    def test_delete_app(self) -> None:
        """
        Test the Client_v2.delete_app method.
        """

        self.requests_mock.delete(f'{self.URL}{self.PATH}apps/does/notexist',
                                  status_code=404)
        self.requests_mock.delete(f'{self.URL}{self.PATH}apps/nginx/latest',
                                  status_code=204)

        self.assertFalse(self.client.delete_app('does', 'notexist'))
        self.assertTrue(self.client.delete_app('nginx', 'latest'))

    def test_get_compose(self) -> None:
        """
        Test the Client_v2.get_compose method.
        """

        url = f'{self.URL}{self.PATH}'
        content = '''name: nginx
version: latest

www:
  enable_ssh: true'''
        self.requests_mock.get(f'{url}apps/does/notexist/files/dockerCompose',
                               status_code=404)
        self.requests_mock.get(f'{url}apps/nginx/latest/files/notUsed',
                               headers={'Content-Type': 'text/html'},
                               text='<html><body>No such path</body></html')
        self.requests_mock.get(f'{url}apps/nginx/latest/files/bigboatCompose',
                               headers={'Content-Type': 'text/plain'},
                               text=content)

        self.assertIsNone(self.client.get_compose('does', 'notexist',
                                                  'dockerCompose'))
        self.assertIsNone(self.client.get_compose('nginx', 'latest', 'notUsed'))
        self.assertEqual(self.client.get_compose('nginx', 'latest',
                                                 'bigboatCompose'), content)

    @staticmethod
    def _put_bigboat_compose_handler(request: Request, context: Context) -> str:
        yaml_file = request.body
        try:
            data = yaml.safe_load(yaml_file)
        except yaml.error.YAMLError as yaml_error:
            context.status_code = 400
            context.headers['content-type'] = 'text/plain'
            return f"Problem asserting validity of YAML: {yaml_error}"

        if data['name'] != 'nginx':
            context.status_code = 400
            context.headers['content-type'] = 'application/json'
            return json.dumps({
                'message': 'Name property of Bigboat compose needs to be equal '
                           'to name property of App'
            })

        context.status_code = 201
        return yaml_file

    def test_update_compose(self) -> None:
        """
        Test the Client_v2.update_compose method.
        """

        url = f'{self.URL}{self.PATH}'
        self.requests_mock.put(f'{url}apps/does/notexist/files/dockerCompose',
                               status_code=404)
        self.requests_mock.put(f'{url}apps/nginx/latest/files/notUsed',
                               headers={'Content-Type': 'text/html'},
                               text='<html><body>No such path</body></html')
        self.requests_mock.put(f'{url}apps/nginx/latest/files/bigboatCompose',
                               text=self._put_bigboat_compose_handler)

        self.assertFalse(self.client.update_compose('does', 'notexist',
                                                    'dockerCompose', 'x: y'))
        self.assertFalse(self.client.update_compose('nginx', 'latest',
                                                    'notUsed', 'x: y'))
        with self.assertRaises(ValueError):
            self.client.update_compose('nginx', 'latest', 'bigboatCompose', ':')
        with self.assertRaises(ValueError):
            self.client.update_compose('nginx', 'latest', 'bigboatCompose',
                                       'name: somethingElse\nversion: latest')

        content = '''name: nginx
version: latest

www:
  enable_ssh: true'''
        self.assertTrue(self.client.update_compose('nginx', 'latest',
                                                   'bigboatCompose', content))

    def test_instances(self) -> None:
        """
        Test the Client_v2.instances method.
        """

        self.requests_mock.get(f'{self.URL}{self.PATH}instances',
                               json=[
                                   {
                                       "id": "y7bzwghzP9ouM56g6",
                                       "name": "nginx",
                                   },
                                   {
                                       "id": "ySYXNTPw2ry9XE6nu",
                                       "name": "nginx2",
                                       "state": {
                                           "current": "starting",
                                           "desired": "running"
                                       }
                                   }
                               ])

        instances = self.client.instances()
        instance_data = list(sorted([
            (instance.name, instance.current_state, instance.desired_state)
            for instance in instances
        ]))
        self.assertEqual(instance_data, [
            ('nginx', 'running', None),
            ('nginx2', 'starting', 'running')
        ])

    def test_get_instance(self) -> None:
        """
        Test the Client_v2.get_instance method.
        """

        self.requests_mock.get(f'{self.URL}{self.PATH}instances/qux',
                               status_code=404)
        self.requests_mock.get(f'{self.URL}{self.PATH}instances/no-api-key',
                               status_code=401, json={"message": "No API key"})
        self.requests_mock.get(f'{self.URL}{self.PATH}instances/nginx',
                               json={
                                   "id": "y7bzwghzP9ouM56g6",
                                   "name": "nginx",
                                   "state": {
                                       "current": "starting",
                                       "desired": "running"
                                   },
                                   "app": {
                                       "name": "nginx",
                                       "version": "latest"
                                   },
                                   "services": {
                                       "www": {
                                           "state": "starting"
                                       }
                                   }
                               })

        self.assertIsNone(self.client.get_instance('qux'))
        with self.assertRaises(ValueError):
            self.client.get_instance('no-api-key')

        instance = self.client.get_instance('nginx')
        assert instance is not None
        self.assertEqual(instance.name, 'nginx')
        self.assertEqual(instance.current_state, 'starting')
        self.assertEqual(instance.desired_state, 'running')
        self.assertEqual(instance.application.name, 'nginx')
        self.assertEqual(instance.application.version, 'latest')
        self.assertEqual(instance.services, {'www': {'state': 'starting'}})

    def test_update_instance(self) -> None:
        """
        Test the Client_v2.update_instance method.
        """

        self.requests_mock.put(f'{self.URL}{self.PATH}instances/error',
                               status_code=400, text='error',
                               headers={'content-type': 'text/plain'})
        self.requests_mock.put(f'{self.URL}{self.PATH}instances/nginx',
                               json={
                                   "id": "y7bzwghzP9ouM56g6",
                                   "name": "nginx",
                                   "state": {
                                       "current": "starting",
                                       "desired": "running"
                                   },
                                   "app": {
                                       "name": "nginx",
                                       "version": "latest"
                                   },
                                   "services": {
                                       "www": {
                                           "state": "starting"
                                       }
                                   }
                               })

        with self.assertRaises(ValueError):
            self.client.update_instance('error', 'does', 'notexist')

        instance = self.client.update_instance('nginx', 'nginx', 'latest',
                                               parameters={
                                                   "SETTING": "value"
                                               },
                                               options={
                                                   "storageBucket": "custom"
                                               })
        assert instance is not None

        self.assertEqual(instance.name, 'nginx')
        self.assertEqual(instance.application.name, 'nginx')
        self.assertEqual(instance.application.version, 'latest')
        self.assertEqual(instance.current_state, 'starting')
        self.assertEqual(instance.desired_state, 'running')
        self.assertEqual(instance.services, {'www': {'state': 'starting'}})

    def test_delete_instance(self) -> None:
        """
        Test the Client_v2.delete_instance method.
        """

        self.requests_mock.delete(f'{self.URL}{self.PATH}instances/error',
                                  status_code=400, text='error',
                                  headers={'content-type': 'text/plain'})
        self.requests_mock.delete(f'{self.URL}{self.PATH}instances/nginx',
                                  json={
                                      "id": "y7bzwghzP9ouM56g6",
                                      "name": "nginx",
                                      "state": {
                                          "current": "stopping",
                                          "desired": "stopped"
                                      },
                                      "app": {
                                          "name": "nginx",
                                          "version": "latest"
                                      },
                                      "services": {
                                          "www": {
                                              "state": "stopping"
                                          }
                                      }
                                  })

        with self.assertRaises(ValueError):
            self.client.delete_instance('error')

        instance = self.client.delete_instance('nginx')
        assert instance is not None
        self.assertEqual(instance.name, 'nginx')
        self.assertEqual(instance.application.name, 'nginx')
        self.assertEqual(instance.application.version, 'latest')
        self.assertEqual(instance.current_state, 'stopping')
        self.assertEqual(instance.desired_state, 'stopped')
        self.assertEqual(instance.services, {'www': {'state': 'stopping'}})

    def test_statuses(self) -> None:
        """
        Test the Client_v2.statuses method.
        """

        content = [
            {
                "name": "Available IPs",
                "lastCheck": {
                    "time": 1494245442228,
                    "ISO": "2017-05-08T12:10:42.228Z"
                },
                "description": "Total number of IPs: 190. IPs in use: 19. "
                               "<strong>Available IPs: 171</strong>",
                "details": {
                    "totalIps": 190,
                    "usedIps": 19
                },
                "isOk": True
            },
            {
                "name": "Docker graph: /var/lib/docker",
                "lastCheck": {
                    "time": 1494245487722,
                    "ISO": "2017-05-08T12:11:27.722Z"
                },
                "description": "Total size: 218.2 GB. "
                               "<strong>Available: 96.3 GB</strong>",
                "details": {
                    "total": 234322399232,
                    "used": 130956759040,
                    "free": 103365640192
                },
                "isOk": True
            },
        ]

        self.requests_mock.get(f'{self.URL}{self.PATH}status', json=content)

        self.assertEqual(self.client.statuses(), content)

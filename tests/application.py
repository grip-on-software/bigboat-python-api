"""
Tests for application entity from the API.

Copyright 2017-2020 ICTU
Copyright 2017-2022 Leiden University

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

import unittest
from unittest.mock import MagicMock
from bigboat.client import Client
from bigboat.application import Application

class ApplicationTest(unittest.TestCase):
    """
    Tests for the application definition entity.
    """

    def setUp(self) -> None:
        self.client = MagicMock(spec_set=Client)
        self.application = Application(self.client, 'nginx', 'latest')

    def test_update(self) -> None:
        """
        Test the Application.update method.
        """

        value = self.application.update()
        self.client.update_app.assert_called_once_with('nginx', 'latest')
        self.assertEqual(value, self.client.update_app.return_value)

    def test_delete(self) -> None:
        """
        Test the Application.delete method.
        """

        value = self.application.delete()
        self.client.delete_app.assert_called_once_with('nginx', 'latest')
        self.assertEqual(value, self.client.delete_app.return_value)

    def test_start(self) -> None:
        """
        Test the Application.start method.
        """

        value = self.application.start()
        self.client.update_instance.assert_called_once_with('nginx', 'nginx',
                                                            'latest')
        self.assertEqual(value, self.client.update_instance.return_value)

        self.client.update_instance.reset_mock()
        self.application.start('nginx2', options={'hi': 'y'})
        self.client.update_instance.assert_called_once_with('nginx2', 'nginx',
                                                            'latest',
                                                            options={'hi': 'y'})

    def test_repr(self) -> None:
        """
        Test the Application.__repr__ method.
        """

        self.assertEqual(repr(self.application),
                         "Application(name='nginx', version='latest')")

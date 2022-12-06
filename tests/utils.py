"""
Tests for utilities.

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

from typing import Any
import unittest
from bigboat.utils import readonly

@readonly(['name', 'version'], rest='other')
class Item:
    """
    Item with some readonly attributes.
    """

    def __init__(self):
        self._name = 'foo'
        self._version = '1'
        self._rest = 'data'

    def get(self) -> str:
        """
        Retrieve data.
        """

        return self._name

    def __getattr__(self, name: str) -> Any:
        raise AttributeError

class Utils_Test(unittest.TestCase):
    """
    Tests for utilities.
    """

    def test_readonly(self) -> None:
        """
        Test the readonly decorator.
        """

        item = Item()
        self.assertEqual(item.name, 'foo')
        self.assertEqual(item.version, '1')
        self.assertEqual(item.other, 'data')
        self.assertEqual(item.get(), 'foo')
        with self.assertRaises(AttributeError):
            dummy = item.nonexistent

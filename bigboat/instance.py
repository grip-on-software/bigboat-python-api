"""
Instance entity from the API.

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

from typing import Any, Dict, List, Optional, Tuple, Union, TYPE_CHECKING
from .entity import Entity
from .utils import readonly
if TYPE_CHECKING: # pragma: no cover
    # pylint: disable=cyclic-import
    from .application import Application
    from .client import Client
else:
    Application = object
    Client = object

@readonly("name", "current_state", "desired_state", "application", "services",
          "parameters", "options")
class Instance(Entity):
    """
    A deployed (parameterized) application instance entity.
    """

    def __init__(self, client: Client, name: str,
                 current_state: Optional[str] = None,
                 **kwargs: Optional[Union[str, Application, Dict[str, Any]]]):
        super().__init__(client)
        self._name = name
        self._current_state = current_state
        self._desired_state = kwargs.get('desired_state')
        self._application = kwargs.get('application')
        self._services = kwargs.get('services')

        self._parameters = kwargs.get('parameters')
        self._options = kwargs.get('options')

    def update(self) -> Optional['Instance']:
        """
        Request the instance to be created with a desired state of 'running'.
        """

        if self.application is None:
            raise ValueError('Application information required to start instance')

        return self.client.update_instance(self.name, self.application.name,
                                           self.application.version,
                                           parameters=self.parameters,
                                           options=self.options)

    def delete(self) -> bool:
        """
        Request the instance to be stopped.
        """

        return self.client.delete_instance(self.name) is not None

    def __repr__(self) -> str:
        parts: List[Tuple[str, Union[str, Application, Dict[str, Any]]]] = [
            ('name', self.name),
            ('current_state', self.current_state),
            ('desired_state', self.desired_state),
            ('application', self.application),
            ('services', self.services),
            ('parameters', self.parameters),
            ('options', self.options)
        ]
        properties = [f'{key}={value!r}' for (key, value) in parts]

        return f'Instance({", ".join(properties)})'

"""
Application entity from the API.

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

from typing import Dict, Optional, TYPE_CHECKING
from .entity import Entity
from .utils import readonly
if TYPE_CHECKING: # pragma: no cover
    # pylint: disable=cyclic-import
    from .client import Client
    from .instance import Instance
else:
    Client = object
    Instance = object

@readonly("name", "version")
class Application(Entity):
    """
    An application definition entity.
    """

    def __init__(self, client: Client, name: str, version: str):
        super().__init__(client)

        self._name = name
        self._version = version

    def update(self) -> Optional['Application']:
        """
        Register the application definition in the BigBoat API.
        """

        return self.client.update_app(self.name, self.version)

    def delete(self) -> bool:
        """
        Delete the application definition in the BigBoat API.
        """

        return self.client.delete_app(self.name, self.version)

    def start(self, name: Optional[str] = None, **kwargs: Dict[str, str]) -> \
            Optional[Instance]:
        """
        Request an instance to be created with a desired state of 'running'
        for this application.

        Args:
            name (:obj:`str` or `None`): The name of the instance to be
                started, or `None` to use the application name.
            **kwargs: Additional properties to use when starting the instance.

        Returns:
            :obj:`bigboat.instance.Instance` or `None`: The instance
            if it was started or `None` if the instance failed to start.
        """

        if name is None:
            name = self.name

        return self.client.update_instance(name, self.name, self.version,
                                           **kwargs)

    def __repr__(self):
        return f'Application(name={self.name!r}, version={self.version!r})'

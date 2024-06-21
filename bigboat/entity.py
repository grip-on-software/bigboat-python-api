"""
Generic base enntity.

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

from typing import Any, Generic, Optional, TypeVar, TYPE_CHECKING
from .utils import readonly
if TYPE_CHECKING: # pragma: no cover
    from .client import Client
else:
    Client = object

EntityT_co = TypeVar('EntityT_co', bound='Entity', covariant=True)

@readonly("client")
class Entity(Generic[EntityT_co]):
    """
    An entity from the BigBoat API.
    """

    def __init__(self, client: Client):
        self._client = client

    def update(self) -> Optional[EntityT_co]:
        """
        Send the data of the entity as an update for its properties to the
        BigBoat API. The entity calls the relevant update method of the client.

        Returns:
            :obj:`bigboat.entity.Entity` or `None`: The updated entity object
            from the API response if it was successfully updated.
        """

        raise NotImplementedError('Must be implemented by subclasses')

    def delete(self) -> bool:
        """
        Delete the entity from the BigBoat API. The entity calls the relevant
        update method of the client.

        Returns:
            bool: Whether the entity was successfully deleted.
        """

        raise NotImplementedError('Must be implemented by subclasses')

    def __getattr__(self, attr: str) -> Any:
        raise AttributeError

"""
Clients that connect to the BigBoat API.

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

from typing import Any, Dict, List, Optional, Union
import requests
from requests.models import Response
import yaml
from .application import Application
from .instance import Instance

class Client:
    """
    Generic client base class, enforcing minimum required interface.
    """

    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip('/')

    @property
    def base_url(self) -> str:
        """
        The base URL of the BigBoat instance.
        """

        return self._base_url

    def apps(self) -> List[Application]:
        """
        Retrieve all application definitions from the API.

        Returns:
            :obj:`list` of :obj:`application.Application`
        """

        raise NotImplementedError('Must be implemented by subclasses')

    def get_app(self, name: str, version: str) -> Optional[Application]:
        """
        Retrieve a specific application definition from the API.

        Args:
            name (str): The name of the application
            version (str): The version of the application

        Returns:
            :obj:`bigboat.application.Application` or `None`: The application
            definition if it was found or `None` if the definition does not
            exist.
        """

        raise NotImplementedError('Must be implemented by subclasses')

    def update_app(self, name: str, version: str) -> Optional[Application]:
        """
        Register an application definition in the API.

        Args:
            name (str): The name of the application
            version (str): The version of the application

        Returns:
            :obj:`bigboat.application.Application` or `None`: The application
            definition if it was successfully created.
        """

        raise NotImplementedError('Must be implemented by subclasses')

    def delete_app(self, name: str, version: str) -> bool:
        """
        Delete an application definition in the API.

        Args:
            name (str): The name of the application
            version (str): The version of the application

        Returns:
            bool: Whether the application was successfully deleted.
        """

        raise NotImplementedError('Must be implemented by subclasses')

    def instances(self) -> List[Instance]:
        """
        Retrieve all live instances from the API.

        Returns:
            :obj:`list` of :obj:`bigboat.instance.Instance`
        """

        raise NotImplementedError('Must be implemented by subclasses')

    def get_instance(self, name: str) -> Optional[Instance]:
        """
        Retrieve a specific live instance from the API.

        Args:
            name (str): The name of the instance.

        Returns:
            :obj:`bigboat.instance.Instance` or `None`: The instance
            if it was found or `None` if the instance does not exist.
        """

        raise NotImplementedError('Must be implemented by subclasses')

    def update_instance(self, name: str, app_name: str, version: str,
                        **kwargs: Dict[str, str]) -> Optional[Instance]:
        """
        Request the instance to be created with a desired state of 'running'.

        Args:
            name (str): The name of the instance to be started.
            app_name (str): The name of the application to be started.
            version (str): The version of the application to be started.
            **kwargs: Additional properties to use when starting the instance.

        Returns:
            :obj:`bigboat.instance.Instance` or `None`: The instance
            if it was started or `None` if the instance failed to start.
        """

        raise NotImplementedError('Must be implemented by subclasses')

    def delete_instance(self, name: str) -> Optional[Instance]:
        """
        Delete a specific live instance from the API.

        Args:
            name (str): The name of the instance.

        Returns:
            :obj:`bigboat.instance.Instance` or `None`: The instance
            if it was found or `None` if the instance did not exist.
        """

        raise NotImplementedError('Must be implemented by subclasses')

class Client_v1(Client):
    """
    Client for the deprecated BigBoat v1 API.
    """

    TIMEOUT = 60

    def _format_url(self, path: str) -> str:
        return f'{self._base_url}/api/v1/{path}'

    def _get(self, path: str) -> Response:
        return requests.get(self._format_url(path), timeout=self.TIMEOUT)

    def _delete(self, path: str) -> Response:
        return requests.delete(self._format_url(path), timeout=self.TIMEOUT)

    def apps(self) -> List[Application]:
        return []

    def get_app(self, name: str, version: str) -> Optional[Application]:
        try:
            request = self._get(f'appdef/{name}/{version}')
        except requests.exceptions.ConnectionError:
            return None

        document = yaml.safe_load(request.text)

        return Application(self, document['name'], str(document['version']))

    def update_app(self, name: str, version: str) -> Optional[Application]:
        # Cannot create new apps through v1 API
        return None

    def delete_app(self, name: str, version: str) -> bool:
        request = self._delete(f'appdef/{name}/{version}')

        if request.status_code == 404:
            return False

        return request.status_code == 200

    def instances(self) -> List[Instance]:
        request = self._get('instances')

        if request.status_code == 404:
            return []

        data = request.json()
        return [Instance(self, name) for name in data['instances']]

    def get_instance(self, name: str) -> Optional[Instance]:
        request = self._get(f'state/{name}')

        if request.status_code == 404:
            return None

        state = 'running' if request.text == 'active' else request.text

        return Instance(self, name, state)

    def update_instance(self, name: str, app_name: str, version: str,
                        **kwargs: Dict[str, str]) -> Optional[Instance]:
        request = self._get(f'start-app/{app_name}/{version}/{name}')

        if request.status_code == 404:
            return None

        return Instance(self, name, current_state='running',
                        application=Application(self, app_name, version))

    def delete_instance(self, name: str) -> Optional[Instance]:
        request = self._get(f'stop-app/{name}')

        if request.status_code == 404:
            return None

        return Instance(self, name, 'created')

class Client_v2(Client):
    """
    Client for the BigBoat v2 API.
    """

    TIMEOUT = 60

    def __init__(self, base_url: str, api_key: str):
        super().__init__(base_url)
        self._api_key = api_key
        self._session = requests.Session()
        self._session.headers.update({'api-key': self._api_key})

    def _format_url(self, path: str) -> str:
        return f'{self._base_url}/api/v2/{path}'

    def _get(self, path: str) -> Response:
        return self._session.get(self._format_url(path), timeout=self.TIMEOUT)

    def _put(self, path: str, content_type: Optional[str] = None,
             data: Optional[Union[str, bytes]] = None,
             json: Optional[Any] = None) -> Response:
        headers: Dict[str, str] = {}
        if content_type is not None:
            headers['Content-Type'] = content_type
        elif json is not None:
            headers['Content-Type'] = 'application/json'

        return self._session.put(self._format_url(path), headers=headers,
                                 data=data, json=json, timeout=self.TIMEOUT)

    def _delete(self, path: str) -> Response:
        return self._session.delete(self._format_url(path),
                                    timeout=self.TIMEOUT)

    @staticmethod
    def _check_bad_request(request: Response) -> None:
        # Bad Request should raise an exception
        if request.status_code == 400:
            if request.headers['Content-Type'] == 'application/json':
                response = request.json()
                raise ValueError(response['message'])

            raise ValueError(request.text)

        # Unauthorized should raise an exception
        if request.status_code == 401:
            response = request.json()
            raise ValueError(response['message'])

    def _format_app(self, app: Dict[str, str]) -> Application:
        return Application(self, app['name'], app['version'])

    def apps(self) -> List[Application]:
        request = self._get('apps')
        self._check_bad_request(request)
        return [self._format_app(app) for app in request.json()]

    def get_app(self, name: str, version: str) -> Optional[Application]:
        request = self._get(f'apps/{name}/{version}')
        self._check_bad_request(request)
        if request.status_code == 404:
            return None

        return self._format_app(request.json())

    def update_app(self, name: str, version: str) -> Optional[Application]:
        try:
            request = self._put(f'apps/{name}/{version}')
        except requests.exceptions.ConnectionError:
            return None

        self._check_bad_request(request)
        return self._format_app(request.json())

    def delete_app(self, name: str, version: str) -> bool:
        request = self._delete(f'apps/{name}/{version}')
        self._check_bad_request(request)
        if request.status_code == 404:
            return False

        return True

    def get_compose(self, name: str, version: str, file_name: str) -> \
            Optional[str]:
        """
        Retrieve a docker compose or bigboat compose file for the application.

        Args:
            name (str): The name of the application
            version (str): The version of the application
            file_name (str): 'dockerCompose' or 'bigboatCompose'

        Returns:
            :obj:`str` or `None`: The application definition's docker compose
            file contents if the application was found, or `None` if the
            definition does not exist.
        """

        path = f'apps/{name}/{version}/files/{file_name}'
        request = self._get(path)
        self._check_bad_request(request)
        if request.status_code == 404:
            return None

        content_type = request.headers.get('content-type')
        if content_type not in ('text/plain', 'text/yaml'):
            return None

        return request.text

    def update_compose(self, name: str, version: str, file_name: str,
                       content: Union[str, bytes]) -> bool:
        """
        Update a docker compose or bigboat compose file for the application.

        Args:
            name (str): The name of the application
            version (str): The version of the application
            file_name (str): 'dockerCompose' or 'bigboatCompose'
            content (str or bytes): The file contents

        Returns:
            bool: Whether the compose file was successfully updated.

        Raises:
            ValueError: When the compose file could not be parsed as a valid
            YAML file.
            ValueError: When the bigboatCompose file contains name or version
            properties that do not match the provided application name/verison.
        """

        path = f'apps/{name}/{version}/files/{file_name}'
        request = self._put(path, content_type='text/plain', data=content)
        self._check_bad_request(request)
        if request.status_code == 404:
            return False

        if request.status_code != 201:
            return False

        return True

    def _format_instance(self,
                         instance: Dict[str, Union[str, Dict[str, Any]]]) -> \
            Instance:
        if 'app' in instance and isinstance(instance['app'], dict):
            application = self._format_app(instance['app'])
        else:
            application = None

        services = instance.get('services')
        if not isinstance(services, dict):
            services = None

        state = instance.get('state')
        if not isinstance(state, dict):
            state = {}

        return Instance(self, str(instance.get('name')),
                        current_state=state.get('current', 'running'),
                        desired_state=state.get('desired'),
                        application=application, services=services)

    def instances(self) -> List[Instance]:
        request = self._get('instances')
        self._check_bad_request(request)
        return [self._format_instance(instance) for instance in request.json()]

    def get_instance(self, name: str) -> Optional[Instance]:
        request = self._get(f'instances/{name}')
        self._check_bad_request(request)

        if request.status_code == 404:
            return None

        return self._format_instance(request.json())

    def update_instance(self, name: str, app_name: str, version: str,
                        **kwargs: Dict[str, str]) -> Optional[Instance]:
        data = {
            'app': app_name,
            'version': version,
            'parameters': kwargs.get('parameters') or {},
            'options': kwargs.get('options') or {}
        }
        request = self._put(f'instances/{name}', json=data)

        self._check_bad_request(request)

        return self._format_instance(request.json())

    def delete_instance(self, name: str) -> Optional[Instance]:
        request = self._delete(f'instances/{name}')

        self._check_bad_request(request)

        return self._format_instance(request.json())

    def statuses(self) -> List[Dict[str, Any]]:
        """
        Retrieve all status items reported by BigBoat.

        Returns:
            :obj:`list` of :obj:`dict`: The status items
        """

        request = self._get('status')
        self._check_bad_request(request)
        return request.json()

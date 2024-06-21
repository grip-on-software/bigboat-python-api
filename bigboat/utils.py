"""
Utilities in the BigBoat API library.

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

from functools import partial
from typing import Any, Callable, Sequence, Type, Union

def readonly(*args: Union[str, Sequence[str]], **kwargs: str) -> \
        Callable[[Type], Type]:
    """
    Register readonly properties for member variables of a class instance.

    Args:
        *args: Variable length list of properties to register as providers of
            read-only access to protected member variables with the same name,
            prefixed with an underscore '_'.
        **kwargs: Arbitrary keyword arguments of properties (keywords) to
            register as providers of read-only access to protected member
            variables with the same name as the argument value.

    Returns:
        A decorator function that applies on a class to provide read-only
        member properties.
    """

    if args and not isinstance(args[0], str):
        properties = args[0]
    else:
        properties = [str(arg) for arg in args]

    aliased_properties = kwargs

    def decorator(subject: Type) -> Type:
        """
        Register the properties in the class.

        Args:
            subject: The class instance.

        Returns:
            The altered class instance.
        """

        def _get_property(property_name: str, instance: object) -> Any:
            return getattr(instance, property_name)

        for property_name in properties:
            setattr(subject, property_name,
                    property(fget=partial(_get_property, f'_{property_name}')))
        for variable_name, property_name in aliased_properties.items():
            setattr(subject, property_name,
                    property(fget=partial(_get_property, f'_{variable_name}')))

        return subject

    return decorator

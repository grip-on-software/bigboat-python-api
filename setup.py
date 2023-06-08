#!/usr/bin/env python

"""
Package setup script.

Copyright 2017-2020 ICTU
Copyright 2017-2022 Leiden University
Copyright 2017-2023 Leon Helwerda

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

from setuptools import setup, find_packages

def main() -> None:
    """
    Setup the package.
    """

    setup(name='bigboat',
          version='0.3.0',
          description='BigBoat docker dashboard API',
          long_description='''Python wrapper library for the BigBoat API.
Support for v2 and the deprecated v1 is included.
This API can create, retrieve, update and delete application definitions,
do similar operations for instances and poll for status''',
          author='Leon Helwerda',
          author_email='l.s.helwerda@liacs.leidenuniv.nl',
          url='https://github.com/grip-on-software/bigboat-python-api',
          license='Apache License, Version 2.0',
          packages=find_packages(exclude=['tests*']),
          package_data={'bigboat': ['py.typed']},
          scripts=[],
          include_package_data=True,
          install_requires=[
              'requests>=2.17.3',
              'pyyaml>=3.12'
          ],
          python_requires='>=3',
          test_suite='tests',
          classifiers=[
              'Development Status :: 4 - Beta',
              'Environment :: Web Environment',
              'Intended Audience :: Developers',
              'License :: OSI Approved :: Apache Software License',
              'Operating System :: OS Independent',
              'Programming Language :: Python',
              'Programming Language :: Python :: 3.8',
              'Programming Language :: Python :: 3.11',
              'Topic :: Internet :: WWW/HTTP',
              'Topic :: Software Development :: Libraries :: Python Modules',
              'Topic :: Software Development :: Build Tools'],
          keywords='docker dashboard bigboat api')

if __name__ == "__main__":
    main()

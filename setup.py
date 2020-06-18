# -*- coding: utf-8 -*-
from setuptools import setup  # type: ignore

packages = \
    ['Playwright', 'Playwright.generated', 'Playwright.locators']

package_data = \
    {'': ['*'], 'Playwright': ['wrapper/*', 'wrapper/generated/*']}

install_requires = \
    ['grpcio-tools>=1.29.0,<2.0.0', 'grpcio>=1.29.0,<2.0.0']

setup_kwargs = {
    'name': 'robotframework-browser',
    'version': '0.0.1',
    'description': '',
    'author': 'Mikko Korpela',
    'author_email': 'mikko.korpela@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MarketSquare/robotframework-browser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': {'console_scripts': ['rfbrowser=Playwright.entry:run']},
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

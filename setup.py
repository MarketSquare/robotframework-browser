# -*- coding: utf-8 -*-
from setuptools import setup, find_packages  # type: ignore

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

packages = \
    find_packages(exclude=["utest", "atest"])

package_data = \
    {'': ['*'], 'Browser': ['wrapper/*', 'wrapper/generated/*']}

install_requires = \
    open("requirements.txt").readlines()

setup_kwargs = {
    'name': 'robotframework-browser',
    'version': '0.3.0',
    'description': '',
    'long_description': long_description,
    'long_description_content_type': 'text/markdown',
    'author': 'Mikko Korpela',
    'author_email': 'mikko.korpela@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MarketSquare/robotframework-browser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': {'console_scripts': ['rfbrowser=Browser.entry:run']},
    'python_requires': '>=3.8,<4.0',
    'classifiers': [
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Testing",
        "Framework :: Robot Framework",
        "Framework :: Robot Framework :: Library"
    ]
}


setup(**setup_kwargs)

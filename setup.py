# -*- coding: utf-8 -*-
from setuptools import find_namespace_packages
from setuptools import setup

setup(
    name='salver',
    version='0.0.1',
    description='Yes',
    long_description='long desc',
    author='Opulence',
    author_email='contact@opulence.fr',
    url='http://opulence.wtf',
    license='',
    packages=find_namespace_packages(include=['salver.*']),
    entry_points={},
    install_requires=[
        'coverage==5.5',
        'celery==5.0.5',
        'celery-redbeat==2.0.0',
        'celerybeat-mongo==0.2.0',
        'docker',
        'dynaconf',
        'elasticsearch==7.10.1',
        'httpx==0.16.1',
        'loguru==0.5.3',
        'neo4j==4.2.1',
        'pydantic==1.7.3',
        'pymongo==3.11.3',
        'redis==3.5.3',
    ],
    extras_require={
        'dev': [
            'coverage[toml]',
            'tox==3.23.0',
            'mock==4.0.3',
            'pytest==6.2.2',
            'flake8==3.9.0',
            'black==20.8b1',
            'mypy==0.812',
            'bandit==1.7.0',
            'pydocstyle==6.0.0',
            'pylint==2.7.4',
            'isort==5.8.0',
            'pygount==1.2.4',
        ],
        'api': [
            'dynaconf==3.1.4',
            'fastapi==0.63.0',
            'uvicorn[standard]==0.13.4',
            'celery==5.0.5',
            'redis==3.5.3',
            'python-socketio==4.6.1',
        ],
    },
    python_requires='>=3.8.*, <4',
)

# -*- coding: utf-8 -*-
from setuptools import find_namespace_packages
from setuptools import setup

setup(
    name="opulence",
    version="0.0.1",
    description="Yes",
    long_description="long desc",
    author="Opulence",
    author_email="contact@opulence.fr",
    url="http://opulence.wtf",
    license="",
    packages=find_namespace_packages(include=["opulence.*"]),
    entry_points={},
    install_requires=[
        "dynaconf[yaml]==3.1.2",
        "celery==5.0.5",
        "redis==3.5.3",
        "pydantic==1.7.3",
        "elasticsearch==7.10.1",
        "httpx==0.16.1",
        "docker==4.4.1",
    ],
    extras_require={},
    python_requires=">=3.8.*, <4",
)

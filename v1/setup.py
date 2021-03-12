from setuptools import find_namespace_packages
from setuptools import setup

with open("README.md") as f:
    readme = f.read()

with open("requirements/production.txt") as f:
    requirements = f.read().splitlines()

with open("requirements/development.txt") as f:
    requirements += f.read().splitlines()

setup(
    name="opulence.collectors",
    version="1.1.0",
    description="Collectors service",
    long_description=readme,
    author="Opulence",
    author_email="contact@opulence.fr",
    url="https://github.com/opullence/collectors",
    license=license,
    packages=find_namespace_packages(include=["opulence.*"]),
    entry_points={
        "console_scripts": ["test-collector=opulence.scripts.test_collector:main"],
    },
    install_requires=requirements,
    python_requires=">=3.6.*, <4",
)

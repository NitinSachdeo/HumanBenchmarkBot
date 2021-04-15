#!/usr/bin/env python
"""The setup script"""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = ["keyboard", "rich", "selenium", "webdriver_manager"]

setup(
    author="Nitin Sachdeo",
    author_email="nitinsachdeo@gmail.com",
    python_requires=">=3.9",
    description="A browser automation based bot intended to be the best there ever was on all the tests part of the Human Benchmark.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="humanbenchmark",
    name="humanbenchmarkbot",
    packages=find_packages(include=["humanbenchmark", "humanbenchmark.*"]),
    url="https://github.com/NitinSachdeo/HumanBenchmarkBot",
    version="0.1.0",
    zip_safe=False,
)
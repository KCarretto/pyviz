"""
Setup info used by pip.
"""
from setuptools import setup, find_packages

setup(
    name="pyviz",
    url="https://github.com/kcarretto/pyviz",
    author="Kyle Carretto",
    author_email="kcarretto@gmail.com",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    license="".join(open("./LICENSE").readlines()),
    long_description=open("README.md").read(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)

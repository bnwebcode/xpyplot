from setuptools import setup

__version__ = "0.0.1"


setup(
    name="xpyplot",
    version=__version__,
    description="Python plotting package",
    author="Bojan Nikolic",
    author_email="bojan@bnikolic.co.uk",
    license="BSD-2",
    platforms="any",
    install_requires=[
        "matplotlib>=3.0",
    ],
)

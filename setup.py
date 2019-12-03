from setuptools import setup
import versioneer

__version__ = versioneer.get_version()


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
    py_modules=["xpyplot"],
)

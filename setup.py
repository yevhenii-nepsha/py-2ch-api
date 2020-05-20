from setuptools import setup, find_packages
from os import path

import codecs
import os.path

here = path.abspath(path.dirname(__file__))


def read(rel_path):
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

__version__ = get_version("py_2ch_api/version.py")

if not __version__:
    raise RuntimeError("Cannot find version information")

setup(
    name="py-2ch-api",
    version=__version__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="yevhenii-nepsha",
    author_email="yevhenii.nepsha@gmail.com",
    license="MIT",
    packages=find_packages(include=["py_2ch_api", "py_2ch_api.*"]),
    python_requires=">=3.7, <4",
    install_requires=["requests==2.22.0", "addict==2.2.1", "wget==3.2"],
    extras_require={"dev": ["black"], "test": ["pytest"]},
)

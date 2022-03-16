"""Just Utils"""


# standard imports
import os
from setuptools import setup


def read(file_name):
    """Utility function to read the README file.
    Used for the long_description in setuptools.setup().
    """

    file_path = os.path.join(os.path.dirname(__file__), file_name)
    return open(file_path).read()


setup(
    name = "just-utils",
    version = "0.0.1",
    author = "Julien Dubuc",
    author_email = "",

    description = "Just Utils",
    long_description = read("README.md"),
    license = "",
    url = "",
    keywords = "",
    classifiers = [
        "Topic :: Utilities",
    ],

    packages = ["just"],
    requires = [],

    test_suite = "tests",
)

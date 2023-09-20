import os
import site
site.ENABLE_USER_SITE = os.geteuid() != 0

from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="rivtlib",
    version = "0.0.4",
    author="rhholland",
    author_email = "andrewjcarter@gmail.com",
    description = ("An demonstration of how to create, document, and publish "
                                   "to the cheese shop a5 pypi.org."),
    license = "MIT",
    keywords = "example documentation tutorial",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['an_example_pypi_project', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    packages=[
        "rivtcalc",
        "rivtcalc.unum",
        "rivtcalc.unum.units",
        "rivtcalc.unum.units.si",
        "rivtcalc.scripts",
        "rivtcalc.docs"
    ],
    version='0.8.2-beta.0',
    python_requires='>=3.7',
    license="MIT",
    long_description=open("README.rst").read(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "sympy",
        "pandas",
        "tabulate",
        "matplotlib",
        "jupyter",
        "docutils",
        "xlrd",
        "antlr4-python3-runtime>=4.7,<4.8",
    ],
)

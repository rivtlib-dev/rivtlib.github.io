from setuptools import setup

setup(
    packages=[
        "rivtlib",
        "rivtlib.unum",
        "rivtlib.unum.units",
        "rivtlib.unum.units.si",
        "rivtlib.scripts",
        "rivtlib.docs"
    ],
    python_requires='>=3.8',
)

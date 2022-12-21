from distutils.core import setup

setup(
    name="rivtlib",
    author="rhholland",
    packages=["rivtlib", "rivtlib.unum", "rivtlib.scripts"],
    version="0.8.2-beta.0",
    python_requires=">=3.8",
    license="GPLv3",
    long_description=open("README.md").read(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #    install_requires=[
    #        "numpy",
    #        "sympy",
    #        "pandas",
    #        "tabulate",
    #        "matplotlib",
    #        "jupyter",
    #        "docutils",
    #        "xlrd",
    #        "antlr4-python3-runtime>=4.7,<4.8",
)

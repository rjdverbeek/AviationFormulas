from setuptools import setup, find_packages
from aviationFormula import __version__, name

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=name,
    version=__version__,
    author="Oliver Clemens",
    author_email="sowintuu@aol.com",
    description="A collection of formula around aviation and the globe in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sowintuu/aviationFormula",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)

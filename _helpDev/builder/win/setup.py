from os import path, listdir
from setuptools import setup
import py2exe


def _collect(d: str) -> list[str]:
    return [fp for f in listdir(d) if path.isfile(fp := path.join(d, f))]


setup(
    windows=["win_loader.py"],
    py_modules=["conductor", "values"],
    packages=["modules"],
    options={"py2exe": {"includes": ["modules.mu0", "modules.mu1"]}},  # because these will be loaded dynamically
    data_files=[("docs", _collect("docs")), ("artfs", _collect("artfs"))]  # or then copy them to the "dist" folder
)

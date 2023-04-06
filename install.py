import bpy
import subprocess
import pathlib
import pkgutil
from . import config


def addPip(strLibrary, reinstall=False):
    if pkgutil.find_loader(strLibrary) is None:
        try:
            python_path = bpy.app.binary_path_python
        except AttributeError:
            import sys
            python_path = next(
                (pathlib.Path(sys.prefix)/"bin").glob("python*"))

        sub = subprocess.run([python_path, "-m", "ensurepip"])
        if sub.returncode != 0:
            return False

        mode = "--upgrade"
        if reinstall:
            mode = "--force-reinstall"

        sub = subprocess.run(
            [python_path, "-m", "pip", "install", mode, "--user", strLibrary])
        if sub.returncode != 0:
            return False
        return True


def addPackages():
    for strPackage in config.PIP_PACKAGES:
        addPip(strPackage)

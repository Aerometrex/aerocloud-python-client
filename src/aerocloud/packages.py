import os

from enum import Enum


class AppPackage(Enum):
    # Add packages here as required.
    LASTOOLS = "lastools"


def getPackageDirectory(package: AppPackage, version: str = None):
    "Gets the directory where the specified package is installed."
    varName = f'AZ_BATCH_APP_PACKAGE_{package.value}'

    if version != None:
        varName = f'{varName}#{version}'

    return os.environ[varName]

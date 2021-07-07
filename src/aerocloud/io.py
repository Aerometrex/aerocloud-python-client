import glob
import os

from functools import reduce

TASK_DATA_DIR_ENV_VAR = "TASK_DATA_DIR"
TASK_WORKING_DIR_ENV_VAR = "AZ_BATCH_TASK_WORKING_DIR"
TASK_PARENT_TASK_IDS_ENV_VAR = "PARENT_TASK_IDS"

cwd = os.getcwd()


def getWorkingDirectory():
    return os.environ.get(TASK_WORKING_DIR_ENV_VAR, cwd)


def getDataDirectory():
    return os.environ.get(TASK_DATA_DIR_ENV_VAR, cwd)


def getInputDirectories():
    return map(lambda id: os.path.join(getDataDirectory(), id),
               os.environ.get(TASK_PARENT_TASK_IDS_ENV_VAR, "input").split(","))


def getInputFiles(filter: str = "*.*"):
    dirs = getInputDirectories()
    matches = map(lambda dir: glob.glob(os.path.join(dir, filter)), dirs)
    return reduce(lambda a, b: a + b, matches)


def getResourceFile(name: str):
    return os.path.join(getWorkingDirectory(), name)


def getOutputDirectory():
    return getDataDirectory()

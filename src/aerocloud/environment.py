import glob
import os

from functools import reduce

DEFAULT_LOCAL_WORKSPACE = "C:\\temp\\aerocloud"
WORKSPACE_WORKING_DIR = "wd"
WORKSPACE_DATA_DIR = "data"
WORKSPACE_INPUT_DIR = "input"

NODE_ID_ENV_VAR = "AZ_BATCH_NODE_ID"
TASK_DATA_DIR_ENV_VAR = "TASK_DATA_DIR"
TASK_WORKING_DIR_ENV_VAR = "AZ_BATCH_TASK_WORKING_DIR"
TASK_PARENT_TASK_IDS_ENV_VAR = "PARENT_TASK_IDS"


localWorkspace = DEFAULT_LOCAL_WORKSPACE


def isLocal():
    return os.environ.get(NODE_ID_ENV_VAR) == None


def getLocalWorkspace():
    return localWorkspace


def setLocalWorkspace(path: str):
    global localWorkspace
    localWorkspace = path
    os.makedirs(os.path.join(localWorkspace, WORKSPACE_WORKING_DIR), exist_ok=True)
    os.makedirs(os.path.join(localWorkspace, WORKSPACE_DATA_DIR, WORKSPACE_INPUT_DIR), exist_ok=True)


def getWorkingDirectory():
    return os.path.join(localWorkspace, WORKSPACE_WORKING_DIR) if isLocal() else os.environ.get(TASK_WORKING_DIR_ENV_VAR)


def getDataDirectory():
    return os.path.join(localWorkspace, WORKSPACE_DATA_DIR) if isLocal() else os.environ.get(TASK_DATA_DIR_ENV_VAR)


def getInputDirectories():
    parentTaskIds = [WORKSPACE_INPUT_DIR] if isLocal() else os.environ.get(TASK_PARENT_TASK_IDS_ENV_VAR).split(",")
    return map(lambda id: os.path.join(getDataDirectory(), id), parentTaskIds)


def getInputFiles(filter: str = "*.*"):
    dirs = getInputDirectories()
    matches = map(lambda dir: glob.glob(os.path.join(dir, filter)), dirs)
    return reduce(lambda a, b: a + b, matches)


def getResourceFile(name: str):
    return os.path.join(getWorkingDirectory(), name)


def getOutputDirectory():
    return getDataDirectory()

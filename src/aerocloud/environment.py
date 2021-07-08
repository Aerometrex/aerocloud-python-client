import glob
import os

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


def getInputDirectory():
    # Note: The Python activity can only have a single parent.
    parentTaskId = WORKSPACE_INPUT_DIR if isLocal() else os.environ.get(TASK_PARENT_TASK_IDS_ENV_VAR)
    return os.path.join(getDataDirectory(), parentTaskId)


def getInputFiles(filter: str = "*.*"):
    return glob.glob(os.path.join(getInputDirectory(), filter))


def getResourceFile(name: str):
    return os.path.join(getWorkingDirectory(), name)


def getOutputDirectory():
    return getDataDirectory()

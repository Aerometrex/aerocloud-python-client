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
    return localWorkspace if isLocal() else None


def setLocalWorkspace(path: str = DEFAULT_LOCAL_WORKSPACE, init: bool = True):
    if not isLocal():
        return

    global localWorkspace
    localWorkspace = path

    os.makedirs(localWorkspace, exist_ok=True)

    if init:
        os.makedirs(os.path.join(localWorkspace, WORKSPACE_WORKING_DIR), exist_ok=True)
        os.makedirs(os.path.join(localWorkspace, WORKSPACE_DATA_DIR, WORKSPACE_INPUT_DIR), exist_ok=True)


def getWorkingDirectory():
    workingDirectory = os.path.join(localWorkspace, WORKSPACE_WORKING_DIR) if isLocal() else os.environ.get(TASK_WORKING_DIR_ENV_VAR)

    if not os.path.isdir(workingDirectory):
        print(f'Working directory {workingDirectory} does not exist. Did you forget to initialise your local workspace?')

    return workingDirectory


def getDataDirectory():
    dataDirectory = os.path.join(localWorkspace, WORKSPACE_DATA_DIR) if isLocal() else os.environ.get(TASK_DATA_DIR_ENV_VAR)

    if not os.path.isdir(dataDirectory):
        print(f'Data directory {dataDirectory} does not exist. Did you forget to initialise your local workspace?')

    return dataDirectory


def getInputDirectory():
    # Note: The Python activity can only have a single parent.
    parentTaskId = WORKSPACE_INPUT_DIR if isLocal() else os.environ.get(TASK_PARENT_TASK_IDS_ENV_VAR)
    inputDirectory = os.path.join(getDataDirectory(), parentTaskId)

    if not os.path.isdir(inputDirectory):
        print(f'Input directory {inputDirectory} does not exist. Did you forget to initialise your local workspace?')

    return inputDirectory


def getInputFiles(filter: str = "*.*"):
    return glob.glob(os.path.join(getInputDirectory(), filter))


def getResourceFile(name: str):
    path = os.path.join(getWorkingDirectory(), name)
    return path if os.path.exists(path) else None


def getOutputDirectory():
    outputDirectory = getDataDirectory()

    if not os.path.isdir(outputDirectory):
        print(f'Output directory {outputDirectory} does not exist. Did you forget to initialise your local workspace?')

    return outputDirectory

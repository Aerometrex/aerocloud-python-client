import glob
import os
import sys
from functools import reduce

if len(sys.argv) < 2:
    print("Parent activity IDs should be provided as first argument (in CSV format).", file=sys.stderr)
    exit(-1)

parentActivityIds = sys.argv[1].split(",")

if len(parentActivityIds) == 0:
    print("No parent activity IDs specified!")
    exit(-1)

taskDataDir = os.environ.get("TASK_DATA_DIR")

if taskDataDir is None:
    print("TASK_DATA_DIR environment variable is not set!")
    exit(-1)

taskWorkingDir = os.environ.get("AZ_BATCH_TASK_WORKING_DIR")

if taskWorkingDir is None:
    print("AZ_BATCH_TASK_WORKING_DIR environment variable is not set!")
    exit(-1)

def getInputDirectories():
    return map(lambda id: os.path.join(taskDataDir, id), parentActivityIds)


def getInputFiles(filter="*.*"):
    dirs = getInputDirectories()
    matches = map(lambda dir: glob.glob(os.path.join(dir, filter)), dirs)
    return reduce(lambda a, b: a + b, matches)


def getResourceFile(name):
    return os.path.join(taskWorkingDir, name)

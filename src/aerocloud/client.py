import glob
import os
import sys
from functools import reduce


def fail(message):
    print(message, file=sys.stderr)
    exit(-1)


if len(sys.argv) < 2:
    fail("Parent activity IDs should be provided as first argument (in CSV format).")

parentActivityIds = sys.argv[1].split(",")

if len(parentActivityIds) == 0:
    fail("No parent activity IDs specified!")

taskDataDir = os.environ.get("TASK_DATA_DIR")

if taskDataDir is None:
    fail("TASK_DATA_DIR environment variable is not set!")

taskWorkingDir = os.environ.get("AZ_BATCH_TASK_WORKING_DIR")

if taskWorkingDir is None:
    fail("AZ_BATCH_TASK_WORKING_DIR environment variable is not set!")


def getInputDirectories():
    return map(lambda id: os.path.join(taskDataDir, id), parentActivityIds)


def getInputFiles(filter="*.*"):
    dirs = getInputDirectories()
    matches = map(lambda dir: glob.glob(os.path.join(dir, filter)), dirs)
    return reduce(lambda a, b: a + b, matches)


def getResourceFile(name):
    return os.path.join(taskWorkingDir, name)

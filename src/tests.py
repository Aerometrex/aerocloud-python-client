import aerocloud
import tempfile
import unittest
import os

from aerocloud.packages import AppPackage


class TestInputOutput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # This test class interacts with the file system using a temporary directory.
        cls.taskDir = tempfile.TemporaryDirectory()

        # Create working and data directories.
        cls.workingDir = os.path.join(cls.taskDir.name, "wd")
        cls.dataDir = os.path.join(cls.taskDir.name, "data")

        os.mkdir(cls.workingDir)
        os.mkdir(cls.dataDir)

        # Create a few parent data directories.
        for i in range(1, 3):
            os.mkdir(os.path.join(cls.dataDir, f'parent-{i}'))

        os.environ["AZ_BATCH_TASK_WORKING_DIR"] = cls.workingDir
        os.environ["PARENT_TASK_IDS"] = "parent-1,parent-2,parent-3"
        os.environ["TASK_DATA_DIR"] = cls.dataDir

    @classmethod
    def tearDownClass(cls):
        # Delete temp task dir.
        cls.taskDir.cleanup()

    def test_getInputDirectories(self):
        expected = map(lambda id: os.path.join(self.dataDir, id), ["parent-1", "parent-2", "parent-3"])
        actual = aerocloud.getInputDirectories()
        self.assertListEqual(list(actual), list(expected))

    def test_getInputFiles(self):
        # Create files we expect to match filter.
        yes1 = os.path.join(self.dataDir, "parent-1", "foo.yes")
        yes2 = os.path.join(self.dataDir, "parent-2", "bar.yes")

        expected = [yes1, yes2]

        # Create an additional file that should not match filter.
        no1 = os.path.join(self.dataDir, "parent-1", "foo.no")

        # Create empty files.
        for file in [yes1, no1, yes2]:
            open(file, "x").close()

        actual = aerocloud.getInputFiles("*.yes")
        self.assertListEqual(sorted(actual), sorted(expected))

    def test_getResourceFile(self):
        expected = os.path.join(self.workingDir, "aoi.shp")
        actual = aerocloud.getResourceFile("aoi.shp")
        self.assertEqual(actual, expected)

    def test_getOutputDirectory(self):
        actual = aerocloud.getOutputDirectory()
        self.assertEqual(actual, self.dataDir)


class TestPackages(unittest.TestCase):
    def test_getPackageDirectory_with_version(self):
        actual = aerocloud.getPackageDirectory(AppPackage.LASTOOLS, "1.0")
        self.assertEqual(actual, "AZ_BATCH_APP_PACKAGE_lastools#1.0")

    def test_getPackageDirectory_without_version(self):
        actual = aerocloud.getPackageDirectory(AppPackage.LASTOOLS)
        self.assertEqual(actual, "AZ_BATCH_APP_PACKAGE_lastools")


if __name__ == "__main__":
    unittest.main()

import tempfile
import unittest
import os

from aerocloud import environment, packages
from aerocloud.packages import AppPackage


class TestInputOutput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # This test class interacts with the file system using a temporary directory.
        cls.workspace = tempfile.TemporaryDirectory()
        environment.setLocalWorkspace(cls.workspace.name)

    @classmethod
    def tearDownClass(cls):
        # Delete temp task dir.
        cls.workspace.cleanup()

    def test_getInputDirectories(self):
        expected = [os.path.join(environment.getDataDirectory(), "input")]
        actual = environment.getInputDirectories()
        self.assertListEqual(list(actual), list(expected))

    def test_getInputFiles(self):
        # Create files we expect to match filter.
        yes = os.path.join(environment.getDataDirectory(), "input", "foo.yes")
        no = os.path.join(environment.getDataDirectory(), "input", "foo.no")

        # Create empty files.
        for file in [yes, no]:
            open(file, "x").close()

        actual = environment.getInputFiles("*.yes")
        self.assertListEqual(list(actual), list([yes]))

    def test_getResourceFile(self):
        expected = os.path.join(environment.getWorkingDirectory(), "aoi.shp")
        actual = environment.getResourceFile("aoi.shp")
        self.assertEqual(actual, expected)

    def test_getOutputDirectory(self):
        actual = environment.getOutputDirectory()
        self.assertEqual(actual, environment.getDataDirectory())


class TestPackages(unittest.TestCase):
    def test_getPackageDirectory_with_version(self):
        actual = packages.getPackageDirectory(AppPackage.LASTOOLS, "1.0")
        self.assertEqual(actual, "AZ_BATCH_APP_PACKAGE_lastools#1.0")

    def test_getPackageDirectory_without_version(self):
        actual = packages.getPackageDirectory(AppPackage.LASTOOLS)
        self.assertEqual(actual, "AZ_BATCH_APP_PACKAGE_lastools")


if __name__ == "__main__":
    unittest.main()

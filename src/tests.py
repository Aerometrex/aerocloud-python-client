import tempfile
import unittest
import os

from aerocloud import environment, packages
from aerocloud.environment import NODE_ID_ENV_VAR, WORKSPACE_WORKING_DIR, WORKSPACE_DATA_DIR, WORKSPACE_INPUT_DIR
from aerocloud.packages import AppPackage


class TestWorkspace(unittest.TestCase):
    def setUp(self):
        # This test class interacts with the file system using a temporary directory.
        self.workspace = tempfile.TemporaryDirectory()
        os.environ.pop(NODE_ID_ENV_VAR, None)

    def test_getLocalWorkspace_should_return_workspace_path_when_local(self):
        self.assertIsNotNone(environment.getLocalWorkspace())

    def test_getLocalWorkspace_should_return_none_when_live(self):
        os.environ[NODE_ID_ENV_VAR] = "NODE-123"  # Simulate live environment.
        self.assertIsNone(environment.getLocalWorkspace())

    def test_setLocalWorkspace_should_create_workspace_structure_when_init_true(self):
        environment.setLocalWorkspace(self.workspace.name, True)

        # Workspace should be initialised.
        self.assertTrue(os.path.isdir(self.workspace.name))
        self.assertTrue(os.path.isdir(os.path.join(self.workspace.name, WORKSPACE_WORKING_DIR)))
        self.assertTrue(os.path.isdir(os.path.join(self.workspace.name, WORKSPACE_DATA_DIR)))
        self.assertTrue(os.path.isdir(os.path.join(self.workspace.name, WORKSPACE_DATA_DIR, WORKSPACE_INPUT_DIR)))

    def test_setLocalWorkspace_should_create_workspace_directory_only_when_init_false(self):
        environment.setLocalWorkspace(self.workspace.name, False)

        # Workspace directory should exist but be empty.
        self.assertTrue(os.path.isdir(self.workspace.name))
        self.assertFalse(os.listdir(self.workspace.name))

    def tearDown(self):
        self.workspace.cleanup()


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

    def test_getInputDirectory_should_return_input_path(self):
        expected = os.path.join(environment.getDataDirectory(), WORKSPACE_INPUT_DIR)
        actual = environment.getInputDirectory()
        self.assertEqual(actual, expected)

    def test_getInputFiles_should_return_matching_files_only(self):
        # Create files we expect to match filter.
        include = os.path.join(environment.getDataDirectory(), WORKSPACE_INPUT_DIR, "i_am_a_match.yes")
        exclude = os.path.join(environment.getDataDirectory(), WORKSPACE_INPUT_DIR, "i_am_not_a_match.no")

        # Create empty files.
        for file in [include, exclude]:
            open(file, "x").close()

        actual = environment.getInputFiles("*.yes")
        self.assertListEqual(list(actual), list([include]))

    def test_getResourceFile_should_return_file_path_when_file_exists(self):
        expected = os.path.join(environment.getWorkingDirectory(), "aoi.shp")
        open(expected, "x").close()

        actual = environment.getResourceFile("aoi.shp")
        self.assertEqual(actual, expected)

    def test_getResourceFile_should_return_none_when_file_does_not_exist(self):
        self.assertIsNone(environment.getResourceFile("i_do_not_exist.shp"))

    def test_getOutputDirectory_should_return_output_path(self):
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

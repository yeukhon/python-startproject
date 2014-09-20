import os
import tempfile
import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from python_startproject import main

class TestMainAsFunctions(unittest.TestCase):
    def setUp(self):
        # Creates a temporary directory as a base directory
        self.home_dir = tempfile.mkdtemp()
        self.project_name = "sample"

    def read_setuppy(self, path):
        setuppy_path = self._full_path(path, "setup.py")
        with open(setuppy_path, "r") as f:
            return f.read()

    def _full_path(self, base_dir, dir_name):
        return os.path.join(base_dir, dir_name)

    def assert_dir_created(self, full_path):
        self.assertTrue(
            os.path.exists(full_path))

    def assert_setuppy_is_default(self, path):
        text = self.read_setuppy(path)
        for default in main.DEFAULTS:
            self.assert_setuppy_has(text, default + '=""')

    def assert_setuppy_has(self, text, pattern):
        self.assertTrue(pattern in text)

    @patch("os.getcwd") 
    def test_create_project_with_default_options(self, mk_cwd):
        """Should create the skeleton at the current
        directory and using the name provided."""
        # First, fake current directory to our home_dir
        mk_cwd.return_value = self.home_dir
        main.create_project(self.project_name)

        project_path = self._full_path(self.home_dir,
            self.project_name)
        self.assert_dir_created(project_path)
        self.assert_setuppy_is_default(project_path)

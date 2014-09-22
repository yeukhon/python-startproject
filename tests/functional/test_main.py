import os
import tempfile
import shutil
import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from python_startproject import main

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        # Creates a temporary directory as a base directory
        self.home_dir = tempfile.mkdtemp()
        self.project_name = "sample"

        # Default checklist. These are hardcoded but we can
        # the difference against the code in our tests.
        self.default_version = "0.1"
        self.default_description = ""
        self.default_author = ""
        self.default_packages = "find_packages()"
        self.default_install_requires = ""

    def tearDown(self):
        shutil.rmtree(self.home_dir)

    def read_setuppy(self, path):
        setuppy_path = self._full_path(path, "setup.py")
        with open(setuppy_path, "r") as f:
            return f.read()

    def _full_path(self, base_dir, dir_name):
        return os.path.join(base_dir, dir_name)

    def assert_dir_created(self, full_path):
        self.assertTrue(
            os.path.exists(full_path))

    def assert_name(self, text, pattern):
        self.assertTrue(
            'name="' + pattern + '"' in text
        )

    def assert_version(self, text, pattern):
        self.assertTrue(
            'version="' + pattern + '"' in text
        )

    def assert_description(self, text, pattern):
        self.assertTrue(
            'description="' + pattern + '"' in text
        )

    def assert_author(self, text, pattern):
        self.assertTrue(
            'author="' + pattern + '"' in text
        )

    def assert_packages(self, text, pattern):
        self.assertTrue(
            'packages=' + pattern in text
        )

    def assert_install_requires(self, text, pattern):
        self.assertTrue(
            'install_requires=[' + pattern + ']' in text
        )

    def assert_setuppy_file_used_default(self, path):
        text = self.read_setuppy(path)
        self.assert_setuppy_used_default(text)

    def assert_setuppy_used_default(self, text):
        self.assert_name(text, self.project_name)
        self.assert_version(text, self.default_version)
        self.assert_description(text, self.default_description)
        self.assert_author(text, self.default_author)
        self.assert_packages(text, self.default_packages)
        self.assert_install_requires(text,
            self.default_install_requires)

class TestMainAsFunction(BaseTestCase):

    @patch("os.getcwd") 
    def test_create_project_with_default_options(self, mk_cwd):
        # First, fake current directory to our home_dir
        mk_cwd.return_value = self.home_dir
        main.create_project(self.project_name)

        project_path = self._full_path(self.home_dir,
            self.project_name)
        self.assert_dir_created(project_path)
        self.assert_setuppy_file_used_default(project_path)

    def test_create_project_with_dir_option(self):
        main.create_project(self.project_name,
            dest_dir=self.home_dir)
        project_path = self._full_path(self.home_dir, self.project_name)
        self.assert_dir_created(project_path)
        self.assert_setuppy_file_used_default(project_path)

class TestTemplateSetuppy(BaseTestCase):

    def setUp(self):
        super(TestTemplateSetuppy, self).setUp()
        self.configs = dict(
            name=self.project_name,
            version=self.default_version,
            description=self.default_description,
            author=self.default_author,
            packages=self.default_packages,
            install_requires=self.default_install_requires
        )

    def test_setuppy_with_defaults(self):
        setuppy = main.template_setuppy(self.configs)
        self.assert_setuppy_used_default(setuppy)

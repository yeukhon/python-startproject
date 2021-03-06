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
        self.package_name = "sample_package"

        # Default checklist. These are hardcoded but we can
        # the difference against the code in our tests.
        self.default_version = "0.1"
        self.default_description = ""
        self.default_author = ""
        self.default_packages = "find_packages()"
        self.default_install_requires = ""

        self.project_path = self._full_path(self.home_dir,
            self.project_name)

        self.mk_cwd = patch("os.getcwd").start()
        self.mk_cwd.return_value = self.home_dir

    def tearDown(self):
        shutil.rmtree(self.home_dir)
        self.mk_cwd.stop()

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

    def assert_setuppy_used_default(self, text, **options):
        assertions = {
            "name": self.assert_name,
            "version": self.assert_version,
            "description": self.assert_description,
            "author": self.assert_author,
            "packages": self.assert_packages,
            "install_requires": self.assert_install_requires
        }
        assertions["name"](text,
            options.get("name", self.project_name))
        assertions["version"](text,
            options.get("version", self.default_version))
        assertions["description"](text,
            options.get("description", self.default_description))
        assertions["author"](text,
            options.get("author", self.default_author))
        assertions["packages"](text,
            options.get("packages", self.default_packages))
        assertions["install_requires"](text,
            options.get("install_requires", self.default_install_requires))

    def assert_setuppy_file_used_default_except(self, path, options):
        text = self.read_setuppy(path)
        self.assert_setuppy_used_default(text, **options)

class TestMainAsFunction(BaseTestCase):
    def test_create_project_with_default_options(self):
        # First, fake current directory to our home_dir
        main.create_project(self.project_name)
        self.assert_dir_created(self.project_path)
        self.assert_setuppy_file_used_default(self.project_path)

    def test_create_project_with_dir_option(self):
        main.create_project(self.project_name,
            dest_dir=self.home_dir)
        self.assert_dir_created(self.project_path)
        self.assert_setuppy_file_used_default(self.project_path)

    def test_create_project_converts_dash_name_to_underscore(self):
        expected_name = self.project_name + "_1"
        self.project_name += "-1"
        # Override the default project path
        self.project_path = self._full_path(self.home_dir,
            self.project_name)
        main.create_project(self.project_name)
        self.assert_dir_created(self.project_path)
        self.assert_setuppy_file_used_default_except(
            self.project_path, {"name": expected_name})

    def test_project_name_untouched_when_package_name_is_given(self):
        expected_project_name = self.project_name
        self.project_path = self._full_path(self.home_dir,
            self.project_name)
        main.create_project(self.project_name,
            **{"package_name": self.package_name})
        self.assert_dir_created(self.project_path)
        self.assert_setuppy_file_used_default_except(
            self.project_path, {"name": expected_project_name})

    def test_create_project_specify_version(self):
        version = "0.0"
        main.create_project(self.project_name, version=version)
        self.assert_dir_created(self.project_path)
        self.assert_setuppy_file_used_default_except(
            self.project_path, {"version": version})

    def test_create_project_specify_description(self):
        description = "This is a nice package"
        main.create_project(self.project_name, description=description)
        self.assert_dir_created(self.project_path)
        self.assert_setuppy_file_used_default_except(
            self.project_path, {"description": description})

    def test_specify_author(self):
        author = "Bob"
        main.create_project(self.project_name, author=author)
        self.assert_dir_created(self.project_path)
        self.assert_setuppy_file_used_default_except(
            self.project_path, {"author": author})

    def test_specify_install_requires(self):
        install_requires = ["first", "second"]
        main.create_project(self.project_name,
            install_requires=install_requires)
        self.assert_dir_created(self.project_path)
        self.assert_setuppy_file_used_default_except(
            self.project_path,
            {"install_requires": ",".join(install_requires)})


class TestParseArgs(BaseTestCase):
    def test_use_default(self):
        args = main.parse_args([self.project_name])
        self.assertEqual(args.project_name, self.project_name)

    def test_package_name_is_optional(self):
        args = main.parse_args([self.project_name])
        self.assertEqual(args.package_name, None)

    def test_version_is_default_to_0_dot_1(self):
        args = main.parse_args([self.project_name])
        self.assertEqual(args.version, "0.1")

    def test_description_is_optional(self):
        args = main.parse_args([self.project_name])
        self.assertEqual(args.description, "")

    def test_author_is_optional(self):
        args = main.parse_args([self.project_name])
        self.assertEqual(args.author, "")

    def test_css_to_list_produces_empty_list_on_empty(self):
        result = main.css_to_list(None)
        self.assertEqual(result, [])

    def test_css_to_list_produces_list_on_comma_string(self):
        result = main.css_to_list("1,2")
        self.assertEqual(result, ["1", "2"])

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

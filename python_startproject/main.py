import argparse
import collections
import os
import sys
from codecs import open

import jinja2

Entry = collections.namedtuple("Entry", ["name", "default"])

def set_project_name(project_name):
    return project_name

def set_version(version=None):
    if version:
        return version
    return "0.1"

def set_description(description=None):
    return description or ""

def set_author(author=None):
    return author or ""

def set_author_email(author_email=None):
    return author_email or ""

def set_packages():
    return "find_packages()"

def set_install_requires(requires):
    if requires:
        return ",".join(requires)

SETUPPY_TEMPLATE = """\
from setuptools import setup, find_packages

setup(
    name="{{ name }}",
    version="{{ version }}",
    description="{{ description }}",
    author="{{ author }}",
    packages={{ packages }},
    install_requires=[{{ install_requires }}]
)
"""

#DEFAULTS = [
#    Entry(name="name", default=set_project_name),
#    Entry(name="version", default=set_version),
#    Entry(name="description", default=set_description),
#    Entry(name="author", default=set_author),
#    Entry(name="packages", default=set_packages),
#    Entry(name="install_requires", default=set_install_requires)
#]

def template_setuppy(configs):
    template = jinja2.Template(SETUPPY_TEMPLATE)
    output = template.render(configs)
    return output

#TODO: Maybe don't pass dict-based options, use args from argparse
def create_project(project_name, **options):
    curr_dir = options.get("dest_dir", os.getcwd())
    project_dir = os.path.join(curr_dir, project_name)
    os.mkdir(project_dir)
    setuppy_path = os.path.join(project_dir, "setup.py")

    # Package name must always be a valid Python ID.
    if options.get("package_name"):
        package_name = options["package_name"].replace("-", "_")
    else:
        if "-" in project_name:
            project_name = project_name.replace("-", "_")
        package_name = project_name

    version = options.get("version", "0.1")
    description = options.get("description", "")
    author = options.get("author", "")
    install_requires = options.get("install_requires", "")

    if install_requires:
        install_requires = ",".join(install_requires)

    configs = {
        "name": project_name,
        "version": version,
        "description": description,
        "author": author,
        "packages": "find_packages()",
        "install_requires": install_requires
    }

    setuppy_text = template_setuppy(configs)
    with open(setuppy_path, "w+", encoding='utf-8') as f:
        f.write(setuppy_text)

def parse_args(args):
    parser = argparse.ArgumentParser(description="Generate Python project skeleton")
    parser.add_argument("project_name",
        help="The name of the new Python project. Unless --package-name is specified, \
this name is used (with dashes converted to underscore) as both the name of the \
directory and the name of the actual Python package (the name used to import).")
    parser.add_argument("--package_name", action="store",
        help="--package_name: allows user to specify the actual name of the package. \
Project name can be different. By default if package-name is not specified, \
project name is used and dashes will be converted to underscore and if \
the project name is not a valid Python ID we will raise an exception.")
    parser.add_argument("--version", action="store", default="0.1",
        help="--version: allows user to specify the starting version number. \
By default this is 0.1.")
    parser.add_argument("--description", action="store", default="",
        help="A one-line summary about the project. Default is no summary.")
    parser.add_argument("--author", action="store", default="",
        help="Author name of this project. Default is no author.")
    return parser.parse_args(args)

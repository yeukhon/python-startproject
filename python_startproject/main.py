import collections
import os
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
    author_email=" {{ email }}",
    packages={{ packages }},
    install_requires=[{{ install_requires }}]
)
"""

DEFAULTS = [
    Entry(name="name", default=set_project_name),
    Entry(name="version", default=set_version),
    Entry(name="description", default=set_description),
    Entry(name="author", default=set_author),
    Entry(name="packages", default=set_packages),
    Entry(name="install_requires", default=set_install_requires)
]

def template_setuppy(configs):
    template = jinja2.Template(SETUPPY_TEMPLATE)
    output = template.render(configs)
    print output
    return output

def create_project(project_name):
    curr_dir = os.getcwd()
    project_dir = os.path.join(curr_dir, project_name)
    os.mkdir(project_dir)
    setuppy_path = os.path.join(project_dir, "setup.py")
    with open(setuppy_path, "w+") as f:
        d = DEFAULTS + [""]
        output = '=""\n'.join(d)
        f.write(output)

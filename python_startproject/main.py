import os

DEFAULTS = [
    "name",
    "version",
    "description",
    "author",
    "packages",
    "install_requires"
]

def create_project(project_name):
    curr_dir = os.getcwd()
    project_dir = os.path.join(curr_dir, project_name)
    os.mkdir(project_dir)
    setuppy_path = os.path.join(project_dir, "setup.py")
    with open(setuppy_path, "w+") as f:
        d = DEFAULTS + [""]
        output = '=""\n'.join(d)
        f.write(output)

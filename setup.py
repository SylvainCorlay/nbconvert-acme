import os
import sys

from setuptools import setup
from setuptools.command.develop import develop

try:
    import jupyter_core.paths as jupyter_core_paths
except ModuleNotFoundError:
    jupyter_core_paths = None


class DevelopCmd(develop):

    prefix_targets = [
    ("nbconvert/templates", 'flowkey')
    ]

    def run(self):
        target_dir = os.path.join(sys.prefix, 'share', 'jupyter')
        if jupyter_core_paths:
            #TODO: potentially brittle logic: see https://jupyter.readthedocs.io/en/latest/use/jupyter-directories.html#envvar-JUPYTER_PATH
            target_dir = jupyter_core_paths.jupyter_path()[1]
        target_dir = os.path.join(target_dir)

        for prefix_target, name in self.prefix_targets:
            source = os.path.join('share', 'jupyter', prefix_target, name)
            target = os.path.join(target_dir, prefix_target, name)
            target_subdir = os.path.dirname(target)
            if not os.path.exists(target_subdir):
                os.makedirs(target_subdir)
            rel_source = os.path.relpath(os.path.abspath(source), os.path.abspath(target_subdir))
            try:
                os.remove(target)
            except:
                pass
            #TODO: is this symbolic link needed?
            print(rel_source, '->', target)
            os.symlink(rel_source, target)

        super().run()

###TODO Later: add relative paths of data files to data_files value of setup args
data_files = []
# for prefix_target, name in PREFIX_TARGETS:
#     source = os.path.join('share', 'jupyter', prefix_target, name)
#     for root, dirs, files in os.walk(source):
#         root_files = [os.path.join(root, i) for i in files]
#         data_files.append((root, root_files))

setup_args = {
    'name': 'nbconvert-flowkey',
    'version': '0.1.0',
    'packages': [],
    'data_files': data_files,
    'install_requires': [
    ],
    'author': 'Paul Wlodkowski',
    'author_email': 'paul@flowkey.com',
    'url': 'https://github.com/pawlodkowski/nbconvert-flowkey',
    'cmdclass': {
        'develop': DevelopCmd, #https://stackoverflow.com/a/27820612/17242197
    } if jupyter_core_paths else {},
}

if __name__ == '__main__':
    setup(**setup_args)

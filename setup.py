from setuptools import setup
from setuptools.command.develop import develop
import os
try:
    import jupyter_core.paths as jupyter_core_paths
except:
    jupyter_core_paths = None


pjoin = os.path.join


class DevelopCmd(develop):
    prefix_targets = [
        ("nbconvert/templates", 'acme'),
        ("voila/templates", 'acme')
    ]
    def run(self):
        target_dir = os.path.join(sys.prefix, 'share', 'jupyter')
        if '--user' in sys.prefix:  # TODO: is there a better way to find out?
            target_dir = jupyter_core_paths.user_dir()
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
            print(rel_source, '->', target)
            os.symlink(rel_source, target)

        super(DevelopCmd, self).run()


data_files = []
for root, dirs, files in os.walk('share'):
    root_files = [os.path.join(root, i) for i in files]
    data_files.append((root, root_files))

setup_args = {
    'name': 'nbconvert-acme',
    'version': '0.1.0',
    'packages': [],
    'data_files': data_files,
    'install_requires': [
    ],
    'author': 'Sylvain Corlay',
    'author_email': 'jupyter@googlegroups.com',
    'url': 'https://github.com/SylvainCorlay/nbconvert-acme/',
    'cmdclass': {
        'develop': DevelopCmd,
    } if jupyter_core_paths else {},
}

if __name__ == '__main__':
    setup(**setup_args)

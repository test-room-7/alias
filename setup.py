import os
import sys

from setuptools import setup
from setuptools.command.install import install

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


from alias import ALIASES_DIR_VAR  # noqa: E402
from alias import get_aliases_dir  # noqa: E402


def set_env_var(var, value):
    os.system(f'setx {var} "{value}"')


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)

        if ALIASES_DIR_VAR not in os.environ:
            aliases_dir = get_aliases_dir()
            set_env_var(ALIASES_DIR_VAR, aliases_dir)


setup(
    cmdclass={
        'install': PostInstallCommand,
    }
)

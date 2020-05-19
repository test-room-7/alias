import os

__version__ = '1.1.0'

ALIASES_DIR_VAR = 'ALIASES_DIR'
ALIASES_DIR_MACRO = '%USERPROFILE%\\Documents\\Scripts\\Aliases'


def get_aliases_dir():
    aliases_dir = os.getenv(ALIASES_DIR_VAR)
    if not aliases_dir:
        aliases_dir = os.path.expandvars(ALIASES_DIR_MACRO)
    return aliases_dir

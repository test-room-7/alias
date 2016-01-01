import glob
import os
import re
import sys

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter

ALIASES_DIR_MACRO = '%USERPROFILE%\\Documents\\Scripts\\Aliases'
ALIASES_DIR_VAR = 'ALIASES_DIR'

aliases_dir = os.path.expandvars(ALIASES_DIR_MACRO)

param_pattern = r'\%[0-9\*]'

ALIAS_WILDCARD = '*.cmd'
ALIAS_EXTENSION = '.cmd'

SETUP_PROMPT = '`alias` is not properly insalled. Do you want to fix it (y/N)? '
DESCRIPTION = '''Manage your aliases.

Add alias:
  > alias gdf=git diff %*

Remove alias:
  > alias gdf=

Show aliases:
  > alias
  > alias --verbose
'''


def is_install_allowed():
    answer = 'N'
    while True:
        answer = raw_input(SETUP_PROMPT)
        answer = answer if answer else 'N'
        if answer in 'YyNn':
            break
    return answer in 'Yy'


def set_env_var(var, value):
    os.system('setx {0} "{1}"'.format(var, value))


def check_env_vars():
    global aliases_dir

    if ALIASES_DIR_VAR not in os.environ:
        if not is_install_allowed():
            return

        set_env_var(ALIASES_DIR_VAR, aliases_dir)
    else:
        aliases_dir = os.environ[ALIASES_DIR_VAR]

    path = os.environ['PATH']
    if aliases_dir not in path:
        path = '{0};{1}'.format(path, aliases_dir)
        set_env_var('PATH', path)

    if not is_alias_exists('alias'):
        command = '{0} %*'.format(sys.argv[0])
        add_alias('alias', command)


def get_alias_path(alias):
    return os.path.join(aliases_dir, '{0}{1}'.format(alias, ALIAS_EXTENSION))


def get_alias_command(alias):
    alias_fn = get_alias_path(alias)
    with open(alias_fn, 'r') as fp:
        return fp.readlines()[1]


def get_alias_list():
    path = os.path.join(aliases_dir, ALIAS_WILDCARD)
    return sorted(
        os.path.splitext(os.path.basename(f))[0] for f in glob.iglob(path))


def is_alias_exists(alias):
    alias_fn = get_alias_path(alias)
    return os.path.exists(alias_fn)


def is_alias_valid(alias):
    for char in '\/:*?<>|"':
        if char in alias:
            return False
    return True


def print_aliases(aliases, verbose):
    if verbose:
        for alias in aliases:
            command = get_alias_command(alias)
            print('{0} = {1}'.format(alias, command))
    else:
        print(', '.join(aliases))


def add_alias(alias, command):
    if is_alias_valid(alias):
        alias_fn = get_alias_path(alias)
        if not os.path.exists(aliases_dir):
            os.makedirs(aliases_dir)
        with open(alias_fn, 'w') as fp:
            if not re.search(param_pattern, command):
                print('Warning: %* or %1..9 is missing')
                # command = '{0} %*'.format(command)
            fp.write('@echo off\n')
            fp.write(command)

        print('Added %s' % alias)
    else:
        print('Invalid alias name: {0}'.format(alias))


def del_alias(alias):
    if is_alias_exists(alias):
        alias_fn = get_alias_path(alias)
        os.remove(alias_fn)
        print('Removed %s' % alias)
    else:
        print('Unknown alias: %s' % alias)


def show_aliases(verbose):
    if os.path.exists(aliases_dir):
        aliases = get_alias_list()
        print_aliases(aliases, verbose)
    else:
        print('No aliases')


def show_alias(alias, verbose):
    if os.path.exists(aliases_dir):
        if is_alias_exists(alias):
            print(get_alias_command(alias))
        else:
            aliases = [a for a in get_alias_list() if a.startswith(alias)]
            if len(aliases) > 0:
                print_aliases(aliases, verbose)
            else:
                print('Unknown alias: %s' % alias)
    else:
        print('No aliases')


def parse_alias(string):
    alias, command = string.split('=', 1)
    alias = alias.strip()
    command = command.strip()
    return alias, command


def create_arg_parser():
    arg_parser = ArgumentParser(prog='alias', description=DESCRIPTION,
                                formatter_class=RawTextHelpFormatter)
    arg_parser.add_argument('--verbose', action='store_true',
                            help='Show verbosed alias list')
    return arg_parser


def parse_args(arg_parser):
    args, params = arg_parser.parse_known_args()

    if params:
        string = ' '.join(params)
        if '=' in string:
            if args.verbose:
                arg_parser.error(
                    'argument --verbose: not allowed in this context')
            alias, command = parse_alias(string)
            if command:
                add_alias(alias, command)
            else:
                del_alias(alias)
        else:
            alias = string
            show_alias(alias, args.verbose)
    else:
        show_aliases(args.verbose)


def main():
    check_env_vars()

    arg_parser = create_arg_parser()
    parse_args(arg_parser)
    return 0


if '__main__' == __name__:
    sys.exit(main())

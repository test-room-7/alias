import os
import re
import sys

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter

if 'ALIASES_DIR' in os.environ:
    ALIASES_DIR = os.path.expandvars('%ALIASES_DIR%')
else:
    ALIASES_DIR = os.path.expandvars('%USERPROFILE%\\Documents\\Scripts\\Aliases')

param_pattern = r'\%[0-9\*]'

DESCRIPTION = '''Manage your aliases.

Add alias:
  > alias gdf=git diff $*

Remove alias:
  > alias gdf=

Show aliases:
  > alias
  > alias --verbose
'''


def get_alias_path(alias):
    return os.path.join(ALIASES_DIR, '{0}.bat'.format(alias))


def get_alias_command(alias):
    alias_fn = get_alias_path(alias)
    with open(alias_fn, 'r') as fp:
        return fp.readlines()[1]


def get_alias_list():
    return sorted(os.path.splitext(f)[0] for f in os.listdir(ALIASES_DIR))


def is_alias_exists(alias):
    alias_fn = get_alias_path(alias)
    return os.os.path.exists(alias_fn)


def add_alias(alias, command):
    alias_fn = get_alias_path(alias)
    if not os.path.exists(ALIASES_DIR):
        os.makedirs(ALIASES_DIR)
    with open(alias_fn, 'w') as fp:
        if not re.search(param_pattern, command):
            print 'Warning: %* or %1..9 is missing'
            # command = '{0} %*'.format(command)
        fp.write('@echo off\n')
        fp.write(command)

    print 'Added %s' % alias


def del_alias(alias):
    if is_alias_exists(alias):
        alias_fn = get_alias_path(alias)
        os.remove(alias_fn)
        print 'Removed %s' % alias
    else:
        print 'Unknown alias: %s' % alias


def print_aliases(verbose):
    if os.path.exists(ALIASES_DIR):
        aliases = get_alias_list()
        if verbose:
            for alias in aliases:
                command = get_alias_command(alias)
                print '{0} = {1}'.format(alias, command)
        else:
            print ', '.join(aliases)
    else:
        print 'No aliases'


def print_alias(alias):
    if os.path.exists(ALIASES_DIR):
        if is_alias_exists(alias):
            print get_alias_command(alias)
        else:
            aliases = [a for a in get_alias_list() if a.startswith(alias)]
            if len(aliases) >= 1:
                print ', '.join(aliases)
            else:
                print 'Unknown alias: %s' % alias
    else:
        print 'No aliases'


def parse_alias(string):
    alias, command = string.split('=', 1)
    alias = alias.strip()
    command = command.strip()
    return alias, command


def create_arg_parser():
    arg_parser = ArgumentParser(description=DESCRIPTION,
                            formatter_class=RawTextHelpFormatter)
    arg_parser.add_argument('--verbose', action='store_true',
                        help='Show verbosed alias list')
    return arg_parser


def parse_args(arg_parser):
    args, params = arg_parser.parse_known_args()

    if params:
        string = ' '.join(params)
        if '=' in string:
            alias, command = parse_alias(string)
            if command:
                add_alias(alias, command)
            else:
                del_alias(alias)
        else:
            alias = string
            print_alias(alias)
    else:
        print_aliases(args.verbose)


def main():
    arg_parser = create_arg_parser()
    parse_args(arg_parser)
    return 0


if '__main__' == __name__:
    sys.exit(main())

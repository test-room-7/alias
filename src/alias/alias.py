import glob
import os
import re

from argparse import ArgumentParser, RawTextHelpFormatter

from alias import __version__, get_aliases_dir

prog = 'alias'

param_pattern = r'\%[0-9\*]'

ALIAS_WILDCARD = '*.cmd'
ALIAS_EXTENSION = '.cmd'

SETUP_PROMPT = f'{prog} is not installed. Do you want to install it (y/N)? '
DESCRIPTION = '''Manage your aliases.

Add alias:
  > alias gdf=git diff %*

Delete alias:
  > alias -d gdf

Show aliases:
  > alias
  > alias -v
'''


def get_alias_path(alias):
    aliases_dir = get_aliases_dir()
    return os.path.join(aliases_dir, f'{alias}{ALIAS_EXTENSION}')


def get_alias_command(alias):
    alias_fn = get_alias_path(alias)
    with open(alias_fn, 'r') as fp:
        return fp.readlines()[1]


def get_alias_list():
    aliases_dir = get_aliases_dir()
    if os.path.exists(aliases_dir):
        path = os.path.join(aliases_dir, ALIAS_WILDCARD)
        return sorted(
            os.path.splitext(os.path.basename(f))[0] for f in glob.iglob(path))
    return []


def is_alias_exists(alias):
    alias_fn = get_alias_path(alias)
    return os.path.exists(alias_fn)


def is_alias_valid(alias):
    for char in r'\/:*?<>|"':
        if char in alias:
            return False
    return True


def print_aliases(aliases, verbose):
    if aliases:
        if verbose:
            for alias in aliases:
                command = get_alias_command(alias)
                print(f'{alias} = {command}')
        else:
            print(', '.join(aliases))
    else:
        print('No aliases')


def add_alias(alias, command):
    if is_alias_valid(alias):
        if not re.search(param_pattern, command):
            print('Warning: %* or %1..9 is missing')

        aliases_dir = get_aliases_dir()
        if not os.path.exists(aliases_dir):
            os.makedirs(aliases_dir)

        alias_fn = get_alias_path(alias)
        is_new_alias = not os.path.exists(alias_fn)

        with open(alias_fn, 'w') as fp:
            fp.write('@echo off\n')
            fp.write(command)

        if is_new_alias:
            print(f'Added {alias}')
        else:
            print(f'Updated {alias}')
    else:
        print(f'Invalid alias name: {alias}')


def del_alias(alias):
    if is_alias_exists(alias):
        alias_fn = get_alias_path(alias)
        os.remove(alias_fn)
        print(f'Deleted {alias}')
    else:
        print(f'Unknown alias: {alias}')


def show_aliases(verbose):
    aliases = get_alias_list()
    print_aliases(aliases, verbose)


def show_alias(alias, verbose):
    if is_alias_exists(alias):
        print(get_alias_command(alias))
    else:
        aliases = [a for a in get_alias_list() if a.startswith(alias)]
        if not aliases:
            print_aliases(aliases, verbose)
        else:
            print(f'Unknown alias: {alias}')


def search_aliases(text, verbose):
    aliases = []
    for alias in get_alias_list():
        command = get_alias_command(alias)
        if text in command:
            aliases.append(alias)
    if aliases:
        print_aliases(aliases, verbose)
    else:
        print('No aliases found')


def parse_alias(string):
    alias, command = string.split('=', 1)
    alias = alias.strip()
    command = command.strip()
    return alias, command


def create_arg_parser():
    arg_parser = ArgumentParser(prog=prog, description=DESCRIPTION,
                                formatter_class=RawTextHelpFormatter)
    arg_parser.add_argument('-d', '--delete', metavar='ALIAS',
                            help='Delete the alias')
    arg_parser.add_argument('-s', '--search', metavar='TEXT',
                            help='Search for the text in alias commands')
    arg_parser.add_argument('-v', '--verbose', action='store_true',
                            help='Verbosed output')
    arg_parser.add_argument('--version', action='version',
                            version=f'{prog} v{__version__}')
    return arg_parser


def parse_args(arg_parser):
    args, params = arg_parser.parse_known_args()

    if params:
        string = ' '.join(params)
        if '=' in string:
            if args.verbose:
                arg_parser.error(
                    'argument -v\\--verbose: not allowed in this context')
                return
            alias, command = parse_alias(string)
            if command:
                add_alias(alias, command)
            else:
                arg_parser.error('cannot add empty alias')
        else:
            alias = string
            show_alias(alias, args.verbose)
    elif args.search:
        search_aliases(args.search, args.verbose)
    elif args.delete:
        del_alias(args.delete)
    else:
        show_aliases(args.verbose)


def main():
    arg_parser = create_arg_parser()
    parse_args(arg_parser)
    return 0

import os
import ConfigParser
import re
import subprocess
import sys

from argparse import ArgumentParser

CMDLINE_SECTION = 'cmd.exe'
ALIASES_FILE = os.path.expandvars('%ALIASES_FILE%')
if not ALIASES_FILE:
    ALIASES_FILE = os.path.expandvars(r'%USERPROFILE%\Documents\Scripts\aliases.ini')

param_pattern = r'\$[0-9\*]'


def get_config():
    config = ConfigParser.RawConfigParser()
    config.read(ALIASES_FILE)
    return config


def save_config(config):
    with open(ALIASES_FILE, 'wb') as config_file:
        config.write(config_file)


def reload_aliases():
    doskey = 'doskey /macrofile=%s' % ALIASES_FILE
    subprocess.call(doskey, shell=True)


def add_alias(alias, command):
    config = get_config()
    if not config.has_section(CMDLINE_SECTION):
        config.add_section(CMDLINE_SECTION)
    if not re.search(param_pattern, command):
        print 'Warning: $* or $1..9 is missing'
        command = '{0} $*'.format(command)
    config.set(CMDLINE_SECTION, alias, command)
    save_config(config)
    reload_aliases()
    print 'Added %s' % alias


def del_alias(alias):
    config = get_config()
    if config.has_option(CMDLINE_SECTION, alias):
        config.remove_option(CMDLINE_SECTION, alias)
        save_config(config)
        reload_aliases()
        print 'Removed %s' % alias
    else:
        print 'Unknown alias: %s' % alias


def print_aliases(verbose):
    config = get_config()
    if config.has_section(CMDLINE_SECTION):
        opts = sorted(config.options(CMDLINE_SECTION))
        if verbose:
            for opt in opts:
                print '{0} = {1}'.format(opt, config.get(CMDLINE_SECTION, opt))
        else:
            print ', '.join(opts)
    else:
        print 'No aliases'


def print_alias(alias):
    config = get_config()
    if config.has_section(CMDLINE_SECTION):
        if config.has_option(CMDLINE_SECTION, alias):
            print config.get(CMDLINE_SECTION, alias)
        else:
            aliases = []
            for opt in sorted(config.options(CMDLINE_SECTION)):
                if opt.startswith(alias):
                    aliases.append(opt)
            if len(aliases) > 1:
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


def main():
    parser = ArgumentParser()
    parser.add_argument('--verbose', action='store_true', help='Show verbosed alias list')
    args, params = parser.parse_known_args()

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


if '__main__' == __name__:
    sys.exit(main())

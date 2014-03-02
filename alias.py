import os
import ConfigParser
import sys

CMDLINE_SECTION = 'cmd.exe'
ALIASES_PATH = os.path.expandvars(r'%USERPROFILE%\Documents\Scripts\aliases.ini')


def get_config():
    config = ConfigParser.RawConfigParser()
    config.read(ALIASES_PATH)
    return config


def add_alias(alias, command):
    config = get_config()
    if not config.has_section(CMDLINE_SECTION):
        config.add_section(CMDLINE_SECTION)
    config.set(CMDLINE_SECTION, alias, command)
    with open(ALIASES_PATH, 'wb') as config_file:
        config.write(config_file)


def print_aliases():
    config = get_config()
    if config.has_section(CMDLINE_SECTION):
        opts = sorted(config.options(CMDLINE_SECTION))
        print '\n'.join(opts)
    else:
        print 'No aliases'


def print_alias(alias):
    config = get_config()
    if config.has_section(CMDLINE_SECTION):
        if alias in config.options(CMDLINE_SECTION):
            print config.get(CMDLINE_SECTION, alias)
            return
    print u'Alias %s not found' % alias


def main(args):
    if args:
        param = ' '.join(args)
        if '=' in param:
            alias, command = param.split('=', 1)
            add_alias(alias, command)
        else:
            alias = param
            print_alias(alias)
    else:
        print_aliases()

if '__main__' == __name__:
    sys.exit(main(sys.argv[1:]))

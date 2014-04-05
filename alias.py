import os
import ConfigParser
import sys

CMDLINE_SECTION = 'cmd.exe'
ALIASES_FILE = os.path.expandvars('%ALIASES_FILE%')
if not ALIASES_FILE:
    ALIASES_FILE = os.path.expandvars(r'%USERPROFILE%\Documents\Scripts\aliases.ini')


def get_config():
    config = ConfigParser.RawConfigParser()
    config.read(ALIASES_FILE)
    return config


def save_config(config):
    with open(ALIASES_FILE, 'wb') as config_file:
        config.write(config_file)


def add_alias(alias, command):
    config = get_config()
    if not config.has_section(CMDLINE_SECTION):
        config.add_section(CMDLINE_SECTION)
    config.set(CMDLINE_SECTION, alias, command)
    save_config(config)
    print 'Added %s' % alias


def del_alias(alias):
    config = get_config()
    if config.has_section(CMDLINE_SECTION) and \
       config.has_option(CMDLINE_SECTION, alias):
            config.remove_option(CMDLINE_SECTION, alias)
            save_config(config)
            print 'Removed %s' % alias
    else:
        print 'Unknown alias: %s' % alias


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
    print 'Unknown alias: %s' % alias


def main(args):
    if args:
        param = ' '.join(args)
        if '=' in param:
            alias, command = param.split('=', 1)
            if command:
                add_alias(alias, command)
            else:
                del_alias(alias)
        else:
            alias = param
            print_alias(alias)
    else:
        print_aliases()


if '__main__' == __name__:
    sys.exit(main(sys.argv[1:]))

"""
dataShare

Usage:
  dataShare hello | bye | Init
  dataShare -h | --help
  dataShare --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  dataShare hello

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/monkeydunkey/dataShare
"""


from inspect import getmembers, isclass

from docopt import docopt

#from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import commands
    options = docopt(__doc__)
    print 'options', options
    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():
        if hasattr(commands, k) and v:
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
if __name__ == '__main__':
    main()

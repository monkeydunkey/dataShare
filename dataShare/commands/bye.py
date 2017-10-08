"""The hello command."""


from json import dumps

from .base import Base


class Bye(Base):
    """Say Bye, world!"""

    def run(self):
        print('Bye, world!')
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

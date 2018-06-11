import re


class Author(object):

    def __init__(self, args):
        self.name = args[0].lower()
        self.given_names = re.split(r'\s+', args[1].lower().replace('.', ''))

    def __str__(self):
        return '{} {}'.format(self.name, self.given_names)


def create_author(line):
    aut = Author(line)
    return aut

import argparse


class Manager(object):

    def __init__(self):
        self.argparse = argparse.ArgumentParser()
        self.mappings = {}

    def command(self, f):
        name = f.__name__
        self.argparse.add_argument(name, nargs='+')
        self.mappings[name] = f 
        return f

    def run(self):
        args = vars(self.argparse.parse_args())
        for k, v in args.iteritems():
            if v:
                f = self.mappings[k]
                f(v[1])



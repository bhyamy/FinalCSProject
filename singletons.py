import datetime
import yaml
import sys

if '-v' in sys.argv or '--verbose' in sys.argv:
    def verbose_print(*args):
        # Print each argument separately so caller doesn't need to
        # stuff everything to be printed into a single string
        for arg in args:
            print(arg)
        # new line
        print()
else:
    def verbose_print(*args):
        return None


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    def __init__(self):
        self.__buffer = ''
        self.print = verbose_print

    def log(self, filename=f'exp_time-{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'):
        with open(filename, 'w') as file:
            file.write(self.__buffer)

    def add_to_buffer(self, msg):
        self.__buffer += msg


class Config(metaclass=Singleton):
    def __init__(self):
        self.configs = {}

    def configure(self, confs_file):

        with open(confs_file, "r") as f:
            configurations = yaml.safe_load(f)

        for section in configurations.keys():
            self.configs[section] = configurations[section]

from os.path import abspath

from jinja2 import Environment, PackageLoader

globals = {'abspath': abspath}

env = Environment(
    loader=PackageLoader('no_drama', 'jinja2'),
)

def get_template(name):
    return env.get_template(name, globals=globals)

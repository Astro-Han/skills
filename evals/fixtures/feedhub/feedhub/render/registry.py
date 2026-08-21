"""Name-keyed formatter extension point.

Formatters register themselves at import time. Deployments may import a third-party
module that registers an additional name; nothing here knows the concrete classes.
"""

FORMATTERS = {}


def register(name, factory):
    FORMATTERS[name] = factory


def resolve(name):
    try:
        return FORMATTERS[name]()
    except KeyError:
        raise ValueError("no formatter registered for {}".format(name))

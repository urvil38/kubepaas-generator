import os


def get_env(name, default=""):
    value = os.environ.get(name)
    if value is None:
        return default
    else:
        return value

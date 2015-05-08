from time import time
from math import modf


def microtime(get_as_float=False):
    if get_as_float:
        return time()
    else:
        return '%f %d' % modf(time())
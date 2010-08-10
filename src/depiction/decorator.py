import cProfile as profile
import pstats
from functools import wraps

from django.conf import settings
from pyprof2calltree import convert


def kgrind(filename):
    def fwrapper(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not settings.PROFILING:
                # Profiling is not enabled, so just call the function
                return f(*args, **kwargs)

            profiler = profile.Profile()

            f_ret_val = profiler.runcall(f, *args, **kwargs)

            profiler.create_stats()
            stats = pstats.Stats(profiler)

            convert(stats, filename)

        return wrapper
    return fwrapper

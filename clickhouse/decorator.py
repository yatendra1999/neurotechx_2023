import functools
import logging
from inspect import getmembers


class LoggingDecorators:
    @classmethod
    def get_callable_properties(cls, func: callable):
        keys = ["__name__", "__module__", "__self__"]
        data = [m for m in getmembers(func) if m[0] in keys]
        data_map = {}
        for entry in data:
            data_map[entry[0]] = entry[1]
        return data_map

    @classmethod
    def functional(cls, func: callable):
        @functools.wraps(func)
        def logging_callable(*args, **kwargs):
            functional_info = cls.get_callable_properties(func)
            logging.warning(
                f"Functional Called: {functional_info}, with \n\tPositional Arguments: {list(args)}\n\tKeywork Arguments: {kwargs}"
            )
            return func(*args, **kwargs)

        return logging_callable

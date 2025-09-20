from typing import Callable
from functools import wraps

def signature_checker(func: Callable):

    types = func.__annotations__

    @wraps(func)
    def wrapper(**kwargs):

        for k, v in kwargs.items():
            if not isinstance(v, types[k]):
                raise TypeError(f"Argument {k} must be of type {types[k]}")

        return func(**kwargs)

    return wrapper
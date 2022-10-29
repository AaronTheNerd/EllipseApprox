import multiprocessing
from typing import Any


def process_safe(cls):
    class Wrapper:
        def __init__(self, *args, **kwargs):
            self.decorated_obj = cls(*args, **kwargs)
            self.lock = multiprocessing.Lock()

        def __thread_safe_func(self, func):
            def wrapper(*args, **kwargs):
                with self.lock:
                    result = func(*args, **kwargs)
                return result

            return wrapper

        def __getattribute__(self, __name: str) -> Any:
            try:
                x = super().__getattribute__(__name)
                return x
            except AttributeError:
                pass
            x = self.decorated_obj.__getattribute__(__name)
            if type(x) == type(self.__init__):
                return self.__thread_safe_func(x)
            else:
                return x

    return Wrapper

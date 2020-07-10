from typing import Callable, TypeVar, Any

F = TypeVar('F', bound=Callable)
def actual_kwargs(f: F) -> F:
    """
    Decorator that provides the wrapped function with an attribute 'actual_kwargs'
    containing just those keyword arguments actually passed in to the function.

    source: https://stackoverflow.com/questions/1408818/getting-the-keyword-arguments-actually-passed-to-a-python-method
    """
    def decorator(function):
        def inner(*args, **kwargs):
            inner.actual_kwargs = kwargs
            return function(*args, **kwargs)
        return inner
    return decorator

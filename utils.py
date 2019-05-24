from typing import Iterable

from token import TokenTypes


def check_type_factory(token_types: Iterable[TokenTypes]):
    def check_type(function):
        def wrapper(*args, **kwargs):
            obj = args[0]
            if obj not in token_types:
                raise TokenTypes.TokenTypeException("",
                                                    f"Not suitable token type. "
                                                    f"{obj} must be "
                                                    f"{'or '.join(map(str, token_types))}.")
            return function(obj, *args, **kwargs)

        return wrapper
    return check_type

from typing import TypedDict, Optional
import enum
from datetime import datetime


class ArgNotSet:
    """Sentinel type for annotations, useful when None is not viable.

    Use like this::

        def is_arg_passed(arg: Union[ArgNotSet, None] = NOTSET) -> bool:
            if arg is NOTSET:
                return False
            return True

        is_arg_passed()  # False.
        is_arg_passed(None)  # True.
    """


NOTSET = ArgNotSet()


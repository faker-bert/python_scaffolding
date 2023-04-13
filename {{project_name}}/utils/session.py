import contextlib
from woflow import settings
from typing import Callable
from functools import wraps
from inspect import signature
from sqlalchemy.orm import Session as SASession


@contextlib.contextmanager
def create_session() -> SASession:
    """Contextmanager that will create and teardown a session."""
    session = settings.Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def find_session_index(func: Callable):
    func_params = signature(func).parameters
    try:
        session_args_idx = tuple(func_params).index('session')
    except ValueError:
        raise ValueError(f"Function {func.__qualname__} has no `session` argument") from None
    return session_args_idx


def provide_session(func: Callable[..., callable]) -> Callable[..., callable]:
    session_args_idx = find_session_index(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'session' in kwargs or session_args_idx < len(args):
            return func(*args, **kwargs)

        with create_session() as session:
            return func(*args, session=session, **kwargs)

    return wrapper




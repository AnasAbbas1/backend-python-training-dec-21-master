import os
import re

ENGINES = {}


def get_engine(db):
    import sqlalchemy, os

    if db not in ENGINES:
        ENGINES[db] = sqlalchemy.create_engine(
            'mysql+mysqldb://' + os.environ['ENGINE_' + db] + '?charset=utf8',
            pool_pre_ping=True,
            pool_size=4,
            pool_recycle=600,
        )
    return ENGINES[db]


import pydantic
from humps import camelize


class NoonBaseModel(pydantic.BaseModel):
    def dump(self):
        return self.dict(
            by_alias=True,
            skip_defaults=True,
        )

    @classmethod
    def bind(cls, func):
        setattr(cls, func.__name__, _bind_wrapper(func))

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        alias_generator = camelize


import pydantic
import functools


def unbind(func, cls):
    @functools.wraps(func)
    def wrapper(**kwargs):
        instance = cls(**kwargs)
        return getattr(instance, func.__name__)()

    return wrapper


import inspect


def bind(func):
    return _bind_wrapper(func)


def _bind_wrapper(func):
    spec = inspect.getfullargspec(func)

    @functools.wraps(func)
    def wrapper(self):
        real_args = []
        d = self.dict()

        for arg in spec.args:
            real_args.append(d[arg])
            del d[arg]

        if not spec.varkw:
            d = {}

        return func(*real_args, **d)

    return wrapper

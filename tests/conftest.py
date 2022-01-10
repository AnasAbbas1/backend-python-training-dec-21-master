import logging
import os

import pytest
from jsql import sql

from libutil import util

logger = logging.getLogger(__name__)

pytest.register_assert_rewrite('noonutil.v1.fastapiutil')

assert len(util.ENGINES) == 0, 'engines set up already'


def setup_engine_env(*engine_names):
    import os

    ENGINE_test = os.environ[f'ENGINE_test'].split('/')[0]
    for k, v in list(os.environ.items()):
        if k.startswith('ENGINE_'):
            del os.environ[k]
    os.environ[f'ENGINE_test'] = ENGINE_test + '/'
    os.environ['TESTING'] = 'pytest'
    for engine_name in engine_names:
        os.environ[f'ENGINE_{engine_name}'] = ENGINE_test + '/' + engine_name
        with util.get_engine('test').connect() as conn:
            conn.execute(f'DROP DATABASE IF EXISTS {engine_name}')
            conn.execute(f'CREATE DATABASE {engine_name}')

    assert os.getenv('ENV') in ('dev', 'staging'), 'must be dev/stg'


def setup_spanner_env():
    os.environ['SPANNER_PROJECT_NAME'] = 'noon-test'


setup_engine_env('wishlist')
setup_spanner_env()

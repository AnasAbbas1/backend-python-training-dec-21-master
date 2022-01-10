import logging

import pytest


logger = logging.getLogger(__name__)


@pytest.fixture()
def client():
    from fastapi.testclient import TestClient
    from appwishlist.web import app
    from noonutil.v1 import fastapiutil

    return fastapiutil.ClientProxy(TestClient(app))


@pytest.fixture(scope="session", autouse=True)
def engine_wishlist():
    from libutil import util

    engine = util.get_engine('wishlist')
    assert engine.url.database == f'wishlist'
    import libwishlist

    libwishlist.models.tables.create_all()
    return engine


@pytest.fixture(scope="session", autouse=True)
def fisxtures(engine_wishlist):
    import libwishlist
    from noonutil.v1 import mysqltestkit

    mysqltestkit.load_fixtures('/src/tests/wishlist/data/env.toml', engine_wishlist, libwishlist.models.tables)
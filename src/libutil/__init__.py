import os
import logging
import sentry_sdk

from noonutil.v1 import logutil
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

try:
    assert False
    import sys

    sys.exit('ERROR asserts disabled, exiting')
except AssertionError:
    pass

logutil.basic_config()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.engine').propagate = False

sentry_sdk.init(dsn=os.getenv('SENTRY_DSN'), environment=os.getenv('ENV'), integrations=[SqlalchemyIntegration()])

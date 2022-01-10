
import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.requests import Request

from pydantic import ValidationError as ResponseValidationError
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sqlalchemy.exc import DatabaseError, IntegrityError, OperationalError
from libwishlist import DomainException, Context
from noonutil.v1 import fastapiutil, logsql

logger = logging.getLogger(__name__)

app_params = fastapiutil.get_basic_params('wishlist', Context.env)
app = FastAPI(**app_params)
app.debug = not Context.is_production
g = fastapiutil.get_request_state_proxy(app)

errhandler_400 = fastapiutil.generate_exception_handler(400)
errhandler_400tb = fastapiutil.generate_exception_handler(400, include_traceback=True)
errhandler_500 = fastapiutil.generate_exception_handler(
    500, sentry_level='error', client_error_message="Sorry, something wrong on our side"
)
errhandler_req_validation = fastapiutil.generate_exception_handler(
    400, client_error_message=fastapiutil.request_validation_error_formatter
)
errhandler_integrity = fastapiutil.generate_exception_handler(
    400, client_error_message=fastapiutil.integrity_error_formatter
)
errhandler_assertion = fastapiutil.generate_exception_handler(
    400, include_traceback=True, client_error_message=fastapiutil.assertion_formatter
)
errhandler_http = fastapiutil.generate_exception_handler(400, client_error_message=lambda exc: exc.detail)

app.add_exception_handler(RequestValidationError, errhandler_req_validation)
app.add_exception_handler(AssertionError, errhandler_assertion)
app.add_exception_handler(DomainException, errhandler_400tb)
app.add_exception_handler(ResponseValidationError, errhandler_500)
app.add_exception_handler(IntegrityError, errhandler_integrity)
app.add_exception_handler(DatabaseError, errhandler_500)
app.add_exception_handler(OperationalError, errhandler_500)
app.add_exception_handler(HTTPException, errhandler_http)
app.add_exception_handler(Exception, errhandler_500)


@app.middleware('http')
def before_request(request: Request, call_next):
    if request.url.path != '/public/hc':
        request.state.user_code = request.headers.get('x-forwarded-user')
        request.state.host = request.headers.get('host')
    return call_next(request)


@app.get("/public/hc", status_code=200, tags=['system'])
def health_check():
    return "OK"


logsql.init()

from appwishlist.views import router

app.include_router(router)
app = SentryAsgiMiddleware(app)

from typing import Optional

from django.contrib.auth import authenticate
from django.utils.functional import SimpleLazyObject
from ib_users.models import UserAccount
from oauth2_provider.models import (
    get_access_token_model,
    get_application_model,
)

from graphql_service.auth import get_token_from_request

Application = get_application_model()
AccessToken = get_access_token_model()


class ResolverNotRegistered(Exception):
    pass


class DL:
    def __init__(self):
        pass


class Context:
    def __init__(self, user_id: str, api_key=None):
        self.user_id = user_id
        self.api_key = api_key
        self.loaders = DL()
        self.exec_time = 0


def get_context(user_id: str, api_key: str = None) -> Context:
    return Context(user_id=user_id, api_key=api_key)


def get_context_value(request):
    request.exec_time = 0
    set_app_on_context(request)
    set_auth_on_context(request)
    return request


def get_app(token) -> Optional[Application]:
    application = AccessToken.objects.get(token=token).application
    return application


def set_app_on_context(request):
    request.app = None
    auth_token = get_token_from_request(request)
    if auth_token and len(auth_token) == 30:
        request.app = SimpleLazyObject(lambda: get_app(auth_token))


def get_user(request):
    if not hasattr(request, "_cached_user"):
        request._cached_user = authenticate(request=request)
    return request._cached_user


def set_auth_on_context(request):
    headers = request.headers

    authorization = headers.get("Authorization")
    auth_token = authorization
    if authorization and "Bearer" in authorization:
        auth_token = authorization.split(" ")[1]
    from django.conf import settings
    is_testing_env = settings.STAGE == "local"
    if is_testing_env:
        if not auth_token:
            auth_token = "access_token"
    if not auth_token:
        raise Exception("auth token not provided")
    if "Bearer" in auth_token:
        auth_token = auth_token.split(" ")[1]

    user = AccessToken.objects.get(token=auth_token).user

    request.user = user
    request.user_id = str(user.user_id)
    return request

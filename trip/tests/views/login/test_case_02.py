"""
# TODO: Update test case description
"""
import pytest
from django_swagger_utils.utils.test_utils import TestUtils
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX, URL_BASE_PATH
from ...factories.models import UserFactory, UserAccountFactory, ApplicationFactory


class TestCase01LoginAPITestCase(TestUtils):
    APP_NAME = APP_NAME
    URL_BASE_PATH = URL_BASE_PATH
    OPERATION_NAME = OPERATION_NAME
    REQUEST_METHOD = REQUEST_METHOD
    URL_SUFFIX = URL_SUFFIX
    SECURITY = {}

    @pytest.mark.django_db
    def test_case(self, snapshot):
        user = UserFactory(phone_no="9310533725")
        user_account = UserAccountFactory(user_id="e9ab68e1-95c2-41bc-966d-615a9cfd175d")
        body = {'phone_no': '9310533725'}
        application = ApplicationFactory(name='trip-guru')
        path_params = {}
        query_params = {}
        headers = {}
        response = self.make_api_call(body=body,
                                      path_params=path_params,
                                      query_params=query_params,
                                      headers=headers,
                                      snapshot=snapshot)

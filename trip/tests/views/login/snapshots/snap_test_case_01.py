# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase01LoginAPITestCase.test_case body'] = {
    'access_token': 'access_token',
    'expires_in': '2024-10-29T12:13:43.414',
    'refresh_token': 'refresh_token',
    'scope': 'read write',
    'token_type': 'Bearer'
}

snapshots['TestCase01LoginAPITestCase.test_case status_code'] = '200'

# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase01LoginAPITestCase.test_case body'] = b'<h1>Not Found</h1><p>The requested resource was not found on this server.</p>'

snapshots['TestCase01LoginAPITestCase.test_case status_code'] = '404'

# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_add_destination_with_invalid_admin_user Result'] = {
    'updateDestination': {
        '__typename': 'UserNotAdmin',
        'userId': 'invalid_test_user'
    }
}

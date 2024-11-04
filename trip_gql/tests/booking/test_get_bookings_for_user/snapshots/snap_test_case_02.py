# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_get_bookings_for_user_with_no_bookings Result'] = {
    'getBookingsForUser': {
        '__typename': 'BookingsNotFound',
        'userId': 'test_user'
    }
}

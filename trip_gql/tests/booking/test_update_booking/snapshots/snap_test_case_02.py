# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_update_booking_with_overlapping_dates Result'] = {
    'updateBooking': {
        '__typename': 'BookingNotPossible',
        'hotelId': 1
    }
}

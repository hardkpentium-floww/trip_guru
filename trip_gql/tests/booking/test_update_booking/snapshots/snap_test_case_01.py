# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_update_booking Result'] = {
    'updateBooking': {
        '__typename': 'Booking',
        'checkinDate': '2024-11-09T10:12:30.705308',
        'checkoutDate': '2024-11-13T10:12:30.705312',
        'destinationId': 7046,
        'hotelId': 3609,
        'id': 4058,
        'tariff': None,
        'totalAmount': 8860,
        'userId': 'test_user'
    }
}

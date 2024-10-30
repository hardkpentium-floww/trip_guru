# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_update_booking Result'] = {
    'updateBooking': {
        '__typename': 'Booking',
        'checkinDate': '2024-11-04T17:10:35.867857',
        'checkoutDate': '2024-11-08T17:10:35.867862',
        'destinationId': 5503,
        'hotelId': 4347,
        'id': 6362,
        'tariff': None,
        'totalAmount': 33752,
        'userId': 'test_user'
    }
}

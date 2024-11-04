# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_book_hotel Result'] = {
    'bookHotel': {
        '__typename': 'Booking',
        'checkinDate': '2024-11-04T10:10:31.079784',
        'checkoutDate': '2024-11-07T10:10:31.079786',
        'destinationId': 755,
        'hotelId': 21,
        'id': 1,
        'tariff': 7450,
        'totalAmount': 22350,
        'userId': 'test_user'
    }
}

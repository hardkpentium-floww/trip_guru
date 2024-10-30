# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_book_hotel Result'] = {
    'bookHotel': {
        '__typename': 'Booking',
        'checkinDate': '2024-10-30T15:23:30.908009',
        'checkoutDate': '2024-11-02T15:23:30.908011',
        'destinationId': 9409,
        'hotelId': 8498,
        'id': 1,
        'tariff': 9296,
        'totalAmount': 27888,
        'userId': 'test_user'
    }
}

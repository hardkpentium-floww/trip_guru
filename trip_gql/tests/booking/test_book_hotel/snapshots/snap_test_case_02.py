# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_book_hotel_with_invalid_booking_dates Result'] = {
    'bookHotel': {
        '__typename': 'BookingDateNotValid',
        'checkinDate': '2024-11-07T10:10:39.272494',
        'checkoutDate': '2024-11-04T10:10:39.272500'
    }
}

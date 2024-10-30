# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_book_hotel Result'] = {
    'bookHotel': {
        '__typename': 'BookingDateNotValid',
        'checkinDate': '2024-11-02T15:23:36.517837',
        'checkoutDate': '2024-10-30T15:23:36.517842'
    }
}

# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_update_hotel_with_duplicate_name Result'] = {
    'updateHotel': {
        '__typename': 'HotelWithNameAlreadyExists',
        'hotelName': 'hotel3'
    }
}

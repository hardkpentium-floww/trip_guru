# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_get_hotel_with_invalid_hotel_id Result'] = {
    'getHotel': {
        '__typename': 'HotelNotFound',
        'id': 1
    }
}

# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_book_hotel_with_invalid_destination_id Result'] = {
    'bookHotel': {
        '__typename': 'DestinationNotFound',
        'destinationId': 1
    }
}

# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_update_hotel Result'] = {
    'updateHotel': {
        '__typename': 'Hotel',
        'description': 'this is a hotel',
        'destinationId': None,
        'id': 9638,
        'imageUrls': 'image_urls',
        'name': 'hotel4',
        'tariff': 5000
    }
}

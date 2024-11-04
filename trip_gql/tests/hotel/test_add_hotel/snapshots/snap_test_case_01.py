# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_add_hotel Result'] = {
    'addHotel': {
        '__typename': 'Hotel',
        'description': 'del',
        'destinationId': 9218,
        'id': 1,
        'imageUrls': 'urls',
        'name': 'hotel1',
        'tariff': 1000
    }
}

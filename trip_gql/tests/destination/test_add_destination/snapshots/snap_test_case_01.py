# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_add_destination Result'] = {
    'addDestination': {
        '__typename': 'Destination',
        'description': 'pollution free city',
        'hotels': [
            {
                'description': 'test_hotel_name',
                'destinationId': 1,
                'id': 1,
                'imageUrls': 'test_hotel_images',
                'name': 'testdz_hotel_name',
                'tariff': 2000
            }
        ],
        'id': 1,
        'name': 'Dedlhzxci',
        'tags': 'smog',
        'userId': 'test_user'
    }
}

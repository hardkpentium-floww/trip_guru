# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_add_rating_with_invalid_destination_id Result'] = {
    'addRating': {
        '__typename': 'DestinationNotFound',
        'destinationId': 10000
    }
}

# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_add_rating Result'] = {
    'addRating': {
        '__typename': 'Rating',
        'destinationId': 7361,
        'rating': 3.2,
        'ratingId': 1,
        'review': 'great place',
        'userId': 'test_user'
    }
}

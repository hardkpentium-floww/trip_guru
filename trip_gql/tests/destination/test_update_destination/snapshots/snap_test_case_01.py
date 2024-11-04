# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase.test_add_destination Result'] = {
    'updateDestination': {
        '__typename': 'Destination',
        'description': '123123',
        'id': 3132,
        'name': 'hotel1',
        'tags': 'beachh',
        'userId': 'test_user'
    }
}

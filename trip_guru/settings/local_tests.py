import uuid

from trip_guru.settings.local import *
from trip_guru.settings.base_pg_db import *

DATABASES['default']['TEST'].update({
    'NAME': '/tmp/%s.sqlite3' % str(uuid.uuid4()),
    'ENGINE': 'django.db.backends.sqlite3',
    'CHARSET': 'UTF8'
})


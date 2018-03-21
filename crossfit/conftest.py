import pytest
from collections import OrderedDict

from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'db.json')


@pytest.fixture()
def records_to_try():
    data = [
        [OrderedDict([('record_time', 100)]),
         OrderedDict([('record_time', 100)]),
         OrderedDict([('record_time', 100)]),
         OrderedDict([('record_time', 100)]),
         OrderedDict([('record_time', 100)]),
         ],
        [OrderedDict([('record_time', 100)]),
         OrderedDict([('record_time', 101)]),
         OrderedDict([('record_time', 102)]),
         OrderedDict([('record_time', 103)]),
         OrderedDict([('record_time', 104)])
         ],
        [OrderedDict([('record_time', 100)]),
         OrderedDict([('record_time', 100)]),
         OrderedDict([('record_time', 102)]),
         OrderedDict([('record_time', 103)]),
         OrderedDict([('record_time', 104)])
         ],
        [OrderedDict([('record_time', 101)]),
         OrderedDict([('record_time', 102)]),
         OrderedDict([('record_time', 103)]),
         OrderedDict([('record_time', 104)]),
         OrderedDict([('record_time', 104)])
        ]
    ]
    return data


@pytest.fixture()
def results_to_try():
    data = [
        [OrderedDict([('record_time', 100), ('rank', 1)]),
         OrderedDict([('record_time', 100), ('rank', 1)]),
         OrderedDict([('record_time', 100), ('rank', 1)]),
         OrderedDict([('record_time', 100), ('rank', 1)]),
         OrderedDict([('record_time', 100), ('rank', 1)])
         ],
        [OrderedDict([('record_time', 100), ('rank', 1)]),
         OrderedDict([('record_time', 101), ('rank', 2)]),
         OrderedDict([('record_time', 102), ('rank', 3)]),
         OrderedDict([('record_time', 103), ('rank', 4)]),
         OrderedDict([('record_time', 104), ('rank', 5)])
         ],
        [OrderedDict([('record_time', 100), ('rank', 1)]),
         OrderedDict([('record_time', 100), ('rank', 1)]),
         OrderedDict([('record_time', 102), ('rank', 3)]),
         OrderedDict([('record_time', 103), ('rank', 4)]),
         OrderedDict([('record_time', 104), ('rank', 5)])
         ],
        [OrderedDict([('record_time', 101), ('rank', 1)]),
         OrderedDict([('record_time', 102), ('rank', 2)]),
         OrderedDict([('record_time', 103), ('rank', 3)]),
         OrderedDict([('record_time', 104), ('rank', 4)]),
         OrderedDict([('record_time', 104), ('rank', 4)])
         ]
    ]
    return data

from datetime import datetime

from core.utils import datetime_to_milliseconds


def test_datetime_to_milliseconds():
    dt = datetime(2019, 1, 1)
    assert datetime_to_milliseconds(dt) == 1546300800000

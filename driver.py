from datetime import datetime

class Driver:
    def __init__(
            self,
            driver_id,
            truck,
            current_time,
    ):
        self._driver_id = driver_id
        self._truck = truck
        self._current_time = current_time

    # driver_id should not be mutable
    @property
    def driver_id(self):
        return self._driver_id

    @property
    def truck(self):
        return self._truck

    @truck.setter
    def truck(self, value):
        self._truck = value

    @property
    def current_time(self):
        return self._current_time

    @current_time.setter
    def current_time(self, value):
        if value is None or isinstance(value, datetime):
            self._current_time = value
        else:
            raise ValueError("Time does not match datetime format.")
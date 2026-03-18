from datetime import datetime

class Truck:
    def __init__(
            self,
            current_location,
            mileage,
            departure_time,
            refrigerated_capable
            ):
        self._truck_array = []
        self._current_location = current_location
        self._mileage = mileage
        self._departure_time = departure_time
        self._refrigerated_capable = refrigerated_capable

    # once array is set it should not be mutable
    @property
    def truck_array(self):
        return self._truck_array

    @property
    def current_location(self):
        return self._current_location

    @current_location.setter
    def current_location(self, value):
        self._current_location = value

    @property
    def mileage(self):
        return self._mileage

    @mileage.setter
    def mileage(self, value):
        self._mileage = value

    @property
    def departure_time(self):
        return self._departure_time

    @departure_time.setter
    def departure_time(self, value):
        if value is None or isinstance(value, datetime):
            self._departure_time = value
        else:
            raise ValueError("Time does not match datetime format.")

    @property
    def refrigerated_capable(self):
        return self._refrigerated_capable

    @refrigerated_capable.setter
    def refrigerated_capable(self, value):
        self._refrigerated_capable = value
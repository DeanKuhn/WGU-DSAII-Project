from status import Status
from datetime import datetime

class Package:
    def __init__(
            self,
                 package_id,
                 address,
                 city,
                 state,
                 package_zip,
                 deadline,
                 weight,
                 notes,
                 status,
                 delivery_time = None
                 ):
        self._package_id = package_id
        self._address = address
        self._city = city
        self._state = state
        self._package_zip = package_zip
        self._deadline = deadline
        self._weight = weight
        self._notes = notes
        self._status = status
        self._delivery_time = delivery_time

    # package ID should not be mutable, and therefore only have a getter
    @property
    def package_id(self):
        return self._package_id

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        self._city = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def package_zip(self):
        return self._package_zip

    @package_zip.setter
    def package_zip(self, value):
        self._package_zip = value

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, value):
        self._deadline = value

    @property
    def weight(self):
        return self._weight

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, Status):
            self._status = value
        else:
            raise ValueError("Value does not match status values.")

    @property
    def delivery_time(self):
        return self._delivery_time

    @delivery_time.setter
    def delivery_time(self, value):
        if value is None or isinstance(value, datetime):
            self._delivery_time = value
        else:
            raise ValueError("Time does not match datetime format.")

    def __str__(self):
        details = [
            f"Package ID: {self._package_id}",
            f"Address: {self._address}",
            f"Deadline: {self._deadline}",
            f"Notes: {self._notes}",
            f"Status: {self._status}",
            f"Delivery Time: {self._delivery_time}"
            ]
        return "\n".join(details)
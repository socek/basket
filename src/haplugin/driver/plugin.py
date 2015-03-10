from hatak.plugin import Plugin, RequestPlugin

from .models import Driver


class DriverPlugin(Plugin):

    def __init__(self):
        super().__init__()
        self.groups = []

    def add_unpackers(self):
        self.unpacker.add('driver', lambda req: req.driver)

    def add_request_plugins(self):
        self.add_request_plugin(DriverRequestPlugin)

    def add_group(self, group):
        self.groups.append(group)


class DriverRequestPlugin(RequestPlugin):

    def __init__(self):
        super().__init__('driver')

    def return_once(self):
        driver = Driver(self.request.db)
        for group in self.parent.groups:
            driver.add_group(group)
        return driver

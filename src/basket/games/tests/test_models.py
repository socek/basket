from pytest import fixture, raises

from ..models import StatusBased


class TestStatusBased(object):

    @fixture
    def status(self):
        obj = StatusBased()
        obj._status = StatusBased._avalible_statuses[0]
        return obj

    def test_getter(self, status):
        """
        getter should return value of _status
        """
        assert status.status == StatusBased._avalible_statuses[0]

    def test_setter(self, status):
        """
        setter should set _status value
        """
        status.status = StatusBased._avalible_statuses[1]

        assert status._status == StatusBased._avalible_statuses[1]

    def test_setter_error(self, status):
        """
        setter should raise ValueError when assiging value which is not in the
        StatusBased._avalible_statuses list
        """
        with raises(ValueError):
            status.status = 'wrong value'

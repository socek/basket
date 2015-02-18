from pytest import fixture
from mock import patch

from hatak.testing import RequestFixture

from ..helpers import MenuWidget


class TestMenuWidget(RequestFixture):

    @fixture
    def widget(self, request):
        widget = MenuWidget(request, 'highlited')
        widget.data = {'menu': []}
        widget.registry = request.registry
        return widget

    def test_init(self, widget):
        assert widget.highlighted == 'highlited'

    def test_add_menu(self, widget):
        """
        add_menu should create MenuObject and append it to the .data['menu']
        """
        with patch('basket.menu.helpers.MenuObject', auto_spec=True) as mock:
            result = widget.add_menu('arg')

            assert result == mock.return_value
            mock.assert_called_once_with(widget, 'arg')
            assert widget.data['menu'] == [result]

    def test_make(self, widget):
        """Sanity check."""
        widget.make()

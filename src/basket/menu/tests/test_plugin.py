from pytest import fixture, yield_fixture
from mock import MagicMock, patch

from ..helpers import MenuWidget
from ..plugin import MenuPlugin, MenuControllerPlugin


class TestsMenuPlugin(object):
    prefix_from = MenuPlugin

    @fixture
    def plugin(self):
        return MenuPlugin()

    def test_add_controller_plugins(self, plugin):
        """
        add_controller_plugins should add MenuControllerPlugin to plugins
        """
        with patch.object(plugin, 'add_controller_plugin') as mock:
            plugin.add_controller_plugins()

            mock.assert_called_once_with(MenuControllerPlugin)


class TestMenuControllerPlugin(object):

    @fixture
    def controller(self):
        return MagicMock()

    @fixture
    def parent(self):
        return MagicMock()

    @fixture
    def plugin(self, controller, parent):
        return MenuControllerPlugin(parent, controller)

    @yield_fixture
    def add_helper(self, plugin):
        with patch.object(plugin, 'add_helper') as mock:
            yield mock

    def test_make_helpers_success(self, plugin, add_helper, controller):
        """
        make_helpers should add MenuWidget to helpers if
        controller.menu_highlighted is specyfied.
        """
        controller.menu_highlighted = 'something'

        plugin.make_helpers()

        add_helper.assert_called_once_with('menu', MenuWidget, 'something')

    def test_make_helpers_fail(self, plugin, add_helper, controller):
        """
        make_helpers should do nothing if controller.menu_highlighted is not
        specyfied.
        """
        del(controller.menu_highlighted)

        plugin.make_helpers()

        assert add_helper.called is False

from pytest import fixture
from mock import MagicMock, patch

from ..models import MenuObject


class TestMenuObject(object):

    @fixture
    def request(self):
        return MagicMock()

    @fixture
    def widget(self, request):
        widget = MagicMock()
        widget.request = request
        return widget

    @fixture
    def inits(self):
        return ('name', 'route', 'icon')

    @fixture
    def model(self, widget, inits):
        return MenuObject(widget, *inits)

    def test_init(self, model, widget, request, inits):
        assert model.widget is widget
        assert model.request is request
        assert model.session is request.session
        assert model.highlighted is widget.highlighted
        assert model.name is inits[0]
        assert model.route is inits[1]
        assert model.icon is inits[2]
        assert model.childs == []

    def test_get_url_success(self, request, model):
        """
        .get_url should return route path if specyfied
        """
        assert model.get_url() is request.route_path.return_value

        request.route_path.assert_called_once_with(model.route)

    def test_get_url_fail(self, request, model):
        """
        .get_url should return '#' if route not specyfied
        """
        model.route = None

        assert model.get_url() == '#'

    def test_is_highlited(self, request, model):
        """
        .is_highlited should return True if self.route is poting where
        Menu.highlighted
        """
        model.highlighted = 'route'
        model.route = 'route'
        assert model.is_highlited() is True

    def test_get_icon(self, request, model):
        """
        get_icon should return class name describeing icon
        """
        assert model.get_icon() == 'fa-icon'

    def test_is_visible_success(self, request, model):
        """
        .is_visible should return has_access_to_route when the route is set
        """
        result = model.is_visible()
        assert result is request.user.has_access_to_route.return_value
        request.user.has_access_to_route.assert_called_once_with(model.route)

    def test_is_visible_fail(self, request, model):
        """
        .is_visible should return True if no route specyfied
        """
        model.route = None
        assert model.is_visible() is True

    def test_add_child(self, request, model):
        """
        Should append MenuObject to MenuObject.childs.
        """
        with patch('basket.menu.models.MenuObject') as mock:
            model.add_child('something', kw='arg')

            assert model.childs == [mock.return_value]
            mock.assert_called_once_with(model.widget, 'something', kw='arg')

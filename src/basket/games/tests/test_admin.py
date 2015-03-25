from mock import patch
from pytest import yield_fixture, fixture

from hatak.testing import ControllerFixture
from haplugin.sql.testing import DatabaseFixture

from ..forms import EditScoreForm, EditGameForm
from ..admin import AdminGameListController, GameEditScoreController
from ..admin import AdminGameListScoreController, GameEditController
from ..widgets import ScoreFormWidget


class LocalFixtures(ControllerFixture):

    @yield_fixture
    def get_game(self, controller):
        with patch.object(controller, 'get_game', autospec=True) as mock:
            yield mock


class TestAdminGameListController(LocalFixtures, DatabaseFixture):

    def _get_controller_class(self):
        return AdminGameListController

    def test_make(self, controller, data):
        """
        .make should put games in the data
        """
        with patch.object(controller, 'get_games', autospec=True) as mock:
            controller.make()

            mock.assert_called_once_with()

            assert data['games'] == mock.return_value

    def test_get_games(self, db, controller, fixtures, app):
        """
        .get_games should return all games
        """
        games = controller.get_games()
        assert len(fixtures['Game']) == len(games.all())


class TestGameEditScoreController(LocalFixtures, DatabaseFixture):

    def _get_controller_class(self):
        return GameEditScoreController

    def test_make(self, controller, data, get_game, add_form, redirect):
        """
        .make should put game in the data and validate form if able
        """
        form = add_form.return_value
        form.validate.return_value = False

        controller.make()

        assert data['game'] == get_game.return_value
        add_form.assert_called_once_with(EditScoreForm, widget=ScoreFormWidget)
        form.validate.assert_called_once_with()
        form.read_game.assert_called_once_with(get_game.return_value)
        assert redirect.called is False

    def test_make_when_form_validated(
            self,
            controller,
            get_game,
            redirect,
            add_form,
            matchdict):
        """
        .make should redirect after form was validated
        """
        form = add_form.return_value
        form.validate.return_value = True
        matchdict['obj_id'] = '10'

        controller.make()

        redirect.assert_called_once_with('games:admin_score', obj_id=10)

    def test_get_game_id(self, controller, matchdict):
        """
        .get_game_id should convert matchdict['obj_id'] str value to int
        """
        matchdict['obj_id'] = '10'

        assert controller.get_game_id() == 10

    def test_get_game(self, fixtures, controller, matchdict):
        """
        .get_game should return game with id pointed out by matchdict['obj_id']
        """
        game = fixtures['Game'][3]
        matchdict['obj_id'] = game.id

        result = controller.get_game()

        assert result.id == game.id


class TestAdminGameListScoreController(LocalFixtures, DatabaseFixture):

    def _get_controller_class(self):
        return AdminGameListScoreController

    def test_get_edit_url_name(self, controller):
        """
        .get_edit_url_name should return url name of editing game.
        """
        assert controller.get_edit_url_name() == 'games:admin_score'

    def test_get_header(self, controller):
        """
        .get_header should return label of header text
        """
        assert controller.get_header() == 'Edycja wyników'


class TestGameEditController(LocalFixtures, DatabaseFixture):

    @fixture
    def add_flashmsg(self, request):
        return request.add_flashmsg

    def _get_controller_class(self):
        return GameEditController

    def test_make_on_no_submit(self, controller, get_game, data, add_form):
        """
        .make should put game in data and add form
        """
        form = add_form.return_value
        form.validate.return_value = None

        controller.make()

        assert data['game'] == get_game.return_value
        add_form.assert_called_once_with(EditGameForm)
        form.read_game.assert_called_once_with(get_game.return_value)

    def test_make_on_submit(
            self,
            controller,
            get_game,
            add_form,
            add_flashmsg,
            redirect):
        """
        .make should create flash message and redirect to games:admin_list
        """
        form = add_form.return_value
        form.validate.return_value = True

        controller.make()

        form.validate.assert_called_once_with()
        add_flashmsg.assert_called_once_with('Zapisano', 'info')
        redirect.assert_called_once_with('games:admin_list')

from mock import patch
from pytest import yield_fixture

from hatak.testing import ControllerFixture
from basket.application.tests.fixtures import FixturesFixtures

from ..forms import EditScoreForm
from ..admin import AdminGameListController, GameEditScoreController
from ..widgets import ScoreFormWidget


class TestAdminGameListController(ControllerFixture, FixturesFixtures):

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


class TestGameEditScoreController(ControllerFixture, FixturesFixtures):

    def _get_controller_class(self):
        return GameEditScoreController

    @yield_fixture
    def get_game(self, controller):
        with patch.object(controller, 'get_game', autospec=True) as mock:
            yield mock

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

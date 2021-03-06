from mock import patch, MagicMock
from pytest import yield_fixture

from hatak.testing import ControllerFixture
from haplugin.sql.testing import DatabaseFixture

from ..models import Game
from ..widgets import GameWidget
from ..controllers import GameListController, GameActiveListController


class TestGameListController(ControllerFixture, DatabaseFixture):

    def _get_controller_class(self):
        return GameListController

    @yield_fixture
    def get_game_widgets(self, controller):
        patcher = patch.object(controller, 'get_game_widgets', autospec=True)
        with patcher as mock:
            yield mock

    @yield_fixture
    def get_header(self, controller):
        patcher = patch.object(controller, 'get_header', autospec=True)
        with patcher as mock:
            yield mock

    @yield_fixture
    def get_games(self, controller):
        with patch.object(controller, 'get_games', autospec=True) as mock:
            yield mock

    @yield_fixture
    def GameWidget(self):
        with patch('basket.games.controllers.GameWidget') as mock:
            yield mock

    def test_make(self, controller, get_game_widgets, get_header, data):
        """
        .make should put game widgets and header_text  to data
        """
        controller.make()

        assert data['games'] == get_game_widgets.return_value
        assert data['header_text'] == get_header.return_value

    def test_get_game_widgets(
            self,
            controller,
            get_games,
            GameWidget,
            request):
        """
        .get_game_widgets should return widgets for all the games
        """
        game = MagicMock()
        get_games.return_value = [game]

        result = list(controller.get_game_widgets())

        assert len(result) == 1
        assert result == [GameWidget.return_value]
        GameWidget.assert_called_once_with(request, game)

    def test_get_header(self, controller):
        """
        .get_header is just a configuration
        """
        assert controller.get_header() == 'Wszystkie mecze'

    def test_get_games(self, fixtures, controller):
        """
        .get_games should return games in the order of Game.date
        """
        games = controller.get_games().all()

        assert games[0].id == fixtures['Game'][0].id
        assert games[5].id == fixtures['Game'][5].id


class TestGameActiveListController(ControllerFixture, DatabaseFixture):

    def _get_controller_class(self):
        return GameActiveListController

    def test_get_games(self, fixtures, db, controller):
        """
        .get_games should return only actually running games
        """
        game = Game()
        game.status = 'running'
        game.group_id = 1
        db.add(game)
        db.commit()

        games = controller.get_games().all()

        assert len(games) == 1
        assert game.id == games[0].id

        db.delete(game)

    def test_get_header(self, controller):
        """
        .get_header is just a configuration
        """
        assert controller.get_header() == 'Aktualnie rozgrywane mecze'

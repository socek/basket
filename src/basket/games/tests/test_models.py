from pytest import fixture, raises, yield_fixture
from mock import MagicMock, patch, call

from ..models import StatusBased, Game, Quart
from haplugin.sql.testing import DatabaseFixture


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


class TestGameCreation(DatabaseFixture):

    @fixture
    def game(self):
        return Game()

    @fixture
    def mdb(self):
        return MagicMock()

    @yield_fixture
    def mquarts(self, game):
        patcher = patch.object(game, 'quarts', [MagicMock()])
        with patcher as mock:
            yield mock

    @yield_fixture
    def mcreate_dependencies(self, game):
        patcher = patch.object(game, 'create_dependencies')
        with patcher as mock:
            yield mock

    @yield_fixture
    def dbgame(self, game, db, fixtures):
        game.left_team = fixtures['Team']['Przyjaciele Szymon']
        game.right_team = fixtures['Team']['TG Team']
        game.index = 10
        game.group = fixtures['Group']['Grupa A']
        game.place = fixtures['Place']['Hala Sportowa Tarnowskie Góry']
        quart = Quart()
        quart.index = 2
        quart.game = game
        quart.left_score = 10
        db.add(quart)
        db.commit()

        game.add_to_db_session(db)
        db.commit()
        try:
            yield game
        finally:
            game.delete(db)
            db.commit()

    def test_create_dependencies(self, dbgame):
        """
        .create_dependencies should create missing quarts.
        """
        assert dbgame.quarts[0].index == 0
        assert dbgame.quarts[1].index == 1
        assert dbgame.quarts[2].index == 2
        assert dbgame.quarts[2].left_score == 10
        assert dbgame.quarts[3].index == 3

    def test_add_to_db_session(self, game, mdb, mcreate_dependencies):
        """
        .add_to_db_session should add all quarts and itself to db
        """
        mquart = MagicMock()
        mcreate_dependencies.return_value = [mquart]

        game.add_to_db_session(mdb)

        mcreate_dependencies.assert_called_once_with()
        assert call(mquart) == mdb.add.call_args_list[0]
        assert call(game) == mdb.add.call_args_list[1]

    def test_delete(self, game, mdb, mquarts):
        """
        .delete should delete all quarts and the game itself
        """
        mquart = mquarts[0]

        game.delete(mdb)

        assert call(mquart) == mdb.delete.call_args_list[0]
        assert call(game) == mdb.delete.call_args_list[1]

    def test_get_report(self, dbgame):
        """
        This test is for veryfing if the report is generated properly.
        """
        assert dbgame.get_report() == {
            'date': None,
            'group_name': 'Grupa A',
            'index': 10,
            'left': {
                'quarts': [None, None, 10, None],
                'sum': 10,
                'team': 'Przyjaciele Szymon'
            },
            'place': 'Hala Sportowa Tarnowskie Góry',
            'right': {
                'quarts': [None, None, None, None],
                'sum': 0,
                'team': 'TG Team'
            },
            'status': 'not started'
        }

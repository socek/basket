from pytest import fixture, yield_fixture

from haplugin.sql.testing import TemporaryDriverObject

from basket.games.models import StatusBased
from ..forms import EditScoreFormData, EditScoreGameData, EditScoreForm
from ..models import Game, Quart
from haplugin.sql.testing import DatabaseFixture


class EditScoreFormDataFixtures(object):

    @fixture
    def data(self):
        return EditScoreFormData()


class TestEditScoreFormDataGetQuartScore(EditScoreFormDataFixtures):

    def test_when_quart_has_score(self, data):
        """
        .get_quart_score should return quart scalar if submited data for
        this quart exists
        """
        data['left_quart1'] = 13

        result = data.get_quart_score('left', 1, 10)

        assert result == 3

    def test_when_quart_has_no_score(self, data):
        """
        .get_quart_score should return None if data is not subbmited for this
        quart
        """
        data['left_quart1'] = None

        assert data.get_quart_score('left', 1, 10) is None


class TestEditScoreFormData(EditScoreFormDataFixtures):

    def test_generate_scalars(self, data):
        """
        .generate_scalars should generate scalar scores of all 4 quarts
        """
        data['left_quart0'] = 0
        data['left_quart1'] = 5
        data['left_quart2'] = 10
        data['left_quart3'] = None

        data['right_quart0'] = 2
        data['right_quart1'] = 3
        data['right_quart2'] = 5
        data['right_quart3'] = 7

        result = list(data.generate_scalars())

        index, left, right = result[0]
        assert index == 0
        assert left == 0
        assert right == 2

        index, left, right = result[1]
        assert index == 1
        assert left == 5
        assert right == 1

        index, left, right = result[2]
        assert index == 2
        assert left == 5
        assert right == 2

        index, left, right = result[3]
        assert index == 3
        assert left is None
        assert right == 2


class EditScoreGameDataFixtures(object):

    @fixture
    def game(self):
        return Game()

    @fixture
    def data(self, game):
        return EditScoreGameData(game)

    @fixture
    def quart(self, game):
        quart = Quart()
        game.quarts = [quart]
        return quart


class TestEditScoreGameDataGetQuartScore(EditScoreGameDataFixtures):

    def test_when_quart_has_score(self, game, data, quart):
        """
        .get_quart_score should return summary score if submited data for
        this quart exists
        """
        quart.left_score = 10

        assert data.get_quart_score('left', 0, 5) == 15

    def test_when_quart_has_no_score(self, game, data, quart):
        """
        .get_quart_score should return None if data is not subbmited for this
        quart
        """
        quart.left_score = None

        assert data.get_quart_score('left', 0, 5) is None


class TestEditScoreGameData(EditScoreGameDataFixtures):

    def test_generate_scores(self, game, data, quart):
        """
        .generate_scores should generate summary scores of all 4 quarts
        """
        quart.left_score = 0
        quart.right_score = 2

        quart = Quart()
        quart.left_score = 1
        quart.right_score = 2
        game.quarts.append(quart)

        quart = Quart()
        quart.left_score = 3
        quart.right_score = 5
        game.quarts.append(quart)

        quart = Quart()
        quart.left_score = 7
        quart.right_score = None
        game.quarts.append(quart)

        result = list(data.generate_scores())

        index, left, right = result[0]
        assert index == 0
        assert left == 0
        assert right == 2

        index, left, right = result[1]
        assert index == 1
        assert left == 1
        assert right == 4

        index, left, right = result[2]
        assert index == 2
        assert left == 4
        assert right == 9

        index, left, right = result[3]
        assert index == 3
        assert left == 11
        assert right is None


class TestEditScoreFormMain(DatabaseFixture):

    @fixture
    def form(self, request):
        return EditScoreForm(request)

    @yield_fixture
    def game(self, db, fixtures):
        def prepare(game):
            game.left_team = fixtures['Team']['Przyjaciele Szymon']
            game.right_team = fixtures['Team']['KKS TG']
            game.group = fixtures['Group']['Grupa A']

        with TemporaryDriverObject(self.driver.Game, prepare) as game:
            yield game

    def test_generate_statuses(self, form):
        data = list(form.generate_statuses())
        for index, status in enumerate(StatusBased._avalible_statuses):
            label = StatusBased.labels[status]
            assert data[index] == {
                'label': label,
                'value': status,
            }

    def test_read_game(self, form):
        """
        .read_game should read from Game object and put the data into form
        """
        game = Game()
        game.id = 3
        game.status = 'running'
        quarts = list(game.create_dependencies())
        game.quarts = quarts
        quarts[0].left_score = 10
        quarts[1].right_score = 15

        form.read_game(game)

        data = form.get_data_dict(True)
        data.pop('csrf_token')

        assert data == {
            'game_id': 3,
            'left_quart0': 10,
            'right_quart1': 15,
            'status': 'running'
        }

    def test_on_success(self, game, db, form):
        """
        .on_success should put the data into game and flush the db
        """
        form.read_game(game)

        form.set_value('status', 'running')
        form.set_value('left_quart0', 10)
        form.set_value('right_quart0', '')
        form.set_value('left_quart1', '')
        form.set_value('right_quart1', 15)
        form.set_value('left_quart2', '')
        form.set_value('right_quart2', '')
        form.set_value('left_quart3', '')
        form.set_value('right_quart3', '')

        form.on_success()

        db.refresh(game)

        assert game.status == 'running'
        assert game.quarts[0].left_score == 10
        assert game.quarts[0].right_score is None
        assert game.quarts[1].right_score == 15

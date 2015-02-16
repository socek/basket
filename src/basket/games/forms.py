import re
from formskit.validators import FieldValidator
from formskit.converters import FakeConvert

from haplugin.formskit import PostForm

from .models import Game, StatusBased


class IsDigit(FieldValidator):

    """Will fail if value is not a digit."""

    regex = re.compile('^-{0,1}[0-9]+$')

    def validate_value(self):
        if not self.value:
            return True
        return re.search(self.regex, self.value) is not None


class ToInt(FakeConvert):

    """Converts to int."""

    def convert(self, value):
        try:
            return int(value)
        except ValueError:
            return None

    def convert_back(self, value):
        if value is None:
            return None
        else:
            return str(value)


class EditScoreFormData(dict):

    def get_quart_score(self, side, index, overal_score):
        try:
            return self['%s_quart%d' % (side, index,)] - overal_score
        except TypeError:
            return None

    def generate_scalars(self):
        left_score = 0
        right_score = 0
        for index in range(4):
            left = self.get_quart_score('left', index, left_score)
            right = self.get_quart_score('right', index, right_score)

            yield index, left, right

            if left:
                left_score += left
            if right:
                right_score += right


class EditScoreGameData(object):

    def __init__(self, game):
        self.game = game

    def get_quart_score(self, side, index, overal_score):
        name = '%s_score' % (side,)
        try:
            return getattr(self.game.quarts[index], name) + overal_score
        except TypeError:
            return None

    def generate_scores(self):
        left_score = 0
        right_score = 0
        for index in range(4):
            left = self.get_quart_score('left', index, left_score)
            right = self.get_quart_score('right', index, right_score)

            yield index, left, right

            if left:
                left_score = left
            if right:
                right_score = right


class EditScoreForm(PostForm):

    def create_form(self):
        self.add_field('game_id', ignore=True, convert=ToInt())

        field = self.add_field('status', label="Stan meczu")
        field.data = self.generate_statuses

        self.add_field('left_quart0', validators=[IsDigit()], convert=ToInt())
        self.add_field('left_quart1', validators=[IsDigit()], convert=ToInt())
        self.add_field('left_quart2', validators=[IsDigit()], convert=ToInt())
        self.add_field('left_quart3', validators=[IsDigit()], convert=ToInt())
        self.add_field('right_quart0', validators=[IsDigit()], convert=ToInt())
        self.add_field('right_quart1', validators=[IsDigit()], convert=ToInt())
        self.add_field('right_quart2', validators=[IsDigit()], convert=ToInt())
        self.add_field('right_quart3', validators=[IsDigit()], convert=ToInt())

    def generate_statuses(self):
        for status in StatusBased._avalible_statuses:
            yield {
                'label': StatusBased.labels[status],
                'value': status,
            }

    def read_game(self, game):
        self.set_value('game_id', game.id, force=True)
        self.set_value('status', game.status)
        game = EditScoreGameData(game)
        for index, left, right in game.generate_scores():
            if left:
                self.set_value('left_quart%d' % (index,), left)
            if right:
                self.set_value('right_quart%d' % (index,), right)

    def on_success(self):
        data = self.get_data_dict(True)
        game = self.get_game(data['game_id'])
        data = EditScoreFormData(data)
        for index, left, right in data.generate_scalars():
            game.quarts[index].left_score = left
            game.quarts[index].right_score = right

        game.status = data['status']
        self.db.flush()
        self.db.commit()

    def get_game(self, id_):
        return self.query(Game).filter_by(id=id_).one()

    def generate_scalars_from_game(self, game):
        left_score = 0
        right_score = 0
        for index in range(4):
            try:
                left = game.quarts[index].left_score + left_score
            except TypeError:
                left = None

            try:
                right = game.quarts[index].right_score + right_score
            except TypeError:
                right = None

            yield index, left, right
            if left:
                left_score = left
            if right:
                right_score = right

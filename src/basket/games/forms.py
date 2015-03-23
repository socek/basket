from formskit.field import AvalibleValue
from formskit.validators import IsDigit, IsValueInAvalibleValues
from formskit.converters import ToInt

from haplugin.formskit import PostForm

from .models import StatusBased


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
        except (TypeError, IndexError):
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
        scores = EditScoreGameData(game)
        for index, left, right in scores.generate_scores():
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
        return self.driver.Game.get_by_id(id_)


class EditGameForm(PostForm):

    def create_form(self):
        self.add_field('game_id', ignore=True, convert=ToInt())
        field = self.add_field(
            'left_team_id',
            label='Pierwsza drużyna',
            convert=ToInt(),
            validators=[IsValueInAvalibleValues(True)])
        field.set_avalible_values(self.generate_teams)

        field = self.add_field(
            'right_team_id',
            label='Druga drużyna',
            convert=ToInt(),
            validators=[IsValueInAvalibleValues(True)]
        )
        field.set_avalible_values(self.generate_teams)

        field = self.add_field(
            'group_id',
            label='Grupa',
            convert=ToInt(),
            validators=[IsValueInAvalibleValues()]
        )
        field.set_avalible_values(self.generate_groups)

        field = self.add_field(
            'place_id',
            label='Miejsce',
            convert=ToInt(),
            validators=[IsValueInAvalibleValues()]
        )
        field.set_avalible_values(self.generate_places)

    def read_game(self, game):
        self.set_value('game_id', game.id, force=True)
        self.set_value('left_team_id', game.left_team_id)
        self.set_value('right_team_id', game.right_team_id)
        self.set_value('group_id', game.group_id)
        self.set_value('place_id', game.place_id)

    def generate_teams(self):
        yield AvalibleValue('', '(brak)')
        for team in self.get_teams():
            yield AvalibleValue(team.id, team.name)

    def get_teams(self):
        return self.driver.Team.get_all()

    def generate_groups(self):
        for group in self.get_groups():
            yield AvalibleValue(group.id, group.name)

    def get_groups(self):
        return self.driver.Group.get_all()

    def generate_places(self):
        for place in self.get_places():
            yield AvalibleValue(place.id, place.name)

    def get_places(self):
        return self.driver.Place.get_all()

    def on_success(self):
        data = self.get_data_dict(True)
        game = self.get_game(data['game_id'])
        game.left_team_id = data['left_team_id']
        game.right_team_id = data['right_team_id']
        game.group_id = data['group_id']

        self.db.flush()
        self.db.commit()

    def get_game(self, id_):
        return self.driver.Game.get_by_id(id_)

from hatak.controller import Controller

from .models import Game
from .widgets import GameWidget
from basket.groups.models import Group


class GameListController(Controller):

    template = 'games:list.haml'
    menu_highlighted = 'games:list'

    def make(self):
        self.data['games'] = self.get_game_widgets()

    def get_game_widgets(self):
        for game in self.get_games():
            yield GameWidget(self.request, game)

    def get_games(self):
        return self.query(Game).order_by(Game.date)


class GameActiveListController(GameListController):

    menu_highlighted = 'games:active_list'

    def get_games(self):
        return super().get_games().filter(Game._status == 'running')


class GroupController(Controller):

    template = 'games:group.haml'

    def make(self):
        self.data['group'] = self.group = self.get_group()
        self.data['games'] = self.get_game_widgets()
        self.data['scores'] = self.group.generate_report()

    def get_game_widgets(self):
        for game in self.group.games:
            yield GameWidget(self.request, game)

    def get_games(self):
        return self.group.games


class GroupAController(GroupController):

    menu_highlighted = 'games:group_a'

    def get_group(self):
        return self.db.query(Group).filter(Group.name == 'Grupa A').one()


class GroupBController(GroupController):
    menu_highlighted = 'games:group_b'

    def get_group(self):
        return self.db.query(Group).filter(Group.name == 'Grupa B').one()

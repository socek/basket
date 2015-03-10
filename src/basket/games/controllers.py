from hatak.controller import Controller

from .widgets import GameWidget


class GameListController(Controller):

    template = 'games:list.haml'
    menu_highlighted = 'games:list'

    def make(self):
        self.data['games'] = self.get_game_widgets()
        self.data['header_text'] = self.get_header()

    def get_game_widgets(self):
        for game in self.get_games():
            yield GameWidget(self.request, game)

    def get_games(self):
        return self.driver.Game.get_all()

    def get_header(self):
        return 'Wszystkie mecze'


class GameActiveListController(GameListController):

    menu_highlighted = 'games:active_list'

    def get_games(self):
        return self.driver.Game.get_running()

    def get_header(self):
        return 'Aktualnie rozgrywane mecze'


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
        return self.driver.Group.get_by_name('Grupa A')


class GroupBController(GroupController):
    menu_highlighted = 'games:group_b'

    def get_group(self):
        return self.driver.Group.get_by_name('Grupa B')


class FinalsController(GroupController):
    template = 'games:finals.haml'
    menu_highlighted = 'games:finals'

    def make(self):
        self.data['group'] = self.group = self.get_group()
        self.data['games'] = list(self.get_game_widgets())

    def get_group(self):
        return self.driver.Group.get_by_name('Finały')

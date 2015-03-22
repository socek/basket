from datetime import datetime

from hatak.controller import Controller

from .forms import EditScoreForm, EditGameForm
from .widgets import ScoreFormWidget


class AdminGameListScoreController(Controller):
    permissions = [('game', 'edit'), ]
    template = 'games:edit_list.haml'
    menu_highlighted = 'games:admin_score_list'

    def make(self):
        self.data['games'] = self.get_games()
        self.data['url_name'] = self.get_edit_url_name()
        self.data['header'] = self.get_header()

    def get_games(self):
        return self.driver.Game.get_all_order_by_date()

    def get_edit_url_name(self):
        return 'games:admin_score'

    def get_header(self):
        return 'Edycja wyników'


class GameController(Controller):

    def get_game(self):
        return self.driver.Game.get_by_id(self.get_game_id())

    def get_game_id(self):
        return int(self.matchdict['obj_id'])


class GameEditScoreController(GameController):
    permissions = [('game', 'edit'), ]
    template = 'games:admin_score.haml'
    menu_highlighted = 'games:admin_list'

    def make(self):
        self.data['game'] = game = self.get_game()
        form = self.add_form(EditScoreForm, widget=ScoreFormWidget)
        form.read_game(game)

        if form.validate() is True:
            self.redirect('games:admin_score', obj_id=self.get_game_id())
            self.add_flashmsg(
                'Zapisano ' + datetime.now().strftime('%H:%M:%S'), 'info')


class AdminGameListController(AdminGameListScoreController):

    def get_edit_url_name(self):
        return 'games:admin'

    def get_header(self):
        return 'Edycja meczy'


class GameEditController(GameController):
    permissions = [('game', 'edit'), ]
    template = 'games:edit_game.haml'
    menu_highlighted = 'games:admin_list'

    def make(self):
        self.data['game'] = game = self.get_game()
        form = self.add_form(EditGameForm)
        form.read_game(game)

        if form.validate() is True:
            self.add_flashmsg('Zapisano', 'info')
            self.redirect('games:admin_list')

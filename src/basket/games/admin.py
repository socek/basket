from hatak.controller import Controller, EndController, HTTPFound

from .models import Game
from .forms import EditScoreForm


class AdminGameListController(Controller):
    permissions = [('game', 'edit'), ]
    template = 'games:edit_list.haml'
    menu_highlighted = 'games:admin_list'

    def make(self):
        self.data['games'] = self.get_games()

    def get_games(self):
        return self.query(Game).order_by(Game.date)


class GameEditScoreController(Controller):
    permissions = [('game', 'edit'), ]
    template = 'games:admin_score.haml'
    menu_highlighted = 'games:admin_list'

    def make(self):
        self.data['game'] = game = self.get_game()
        form = self.add_form(EditScoreForm)
        form.read_game(game)

        if form.validate() is True:
            self.redirect('games:admin_score', obj_id=self.get_game_id())

    def get_game(self):
        return self.query(Game).filter_by(id=self.get_game_id()).one()

    def get_game_id(self):
        return int(self.matchdict['obj_id'])

    def redirect(self, to, end=False, **kwargs):
        url = self.request.route_url(to, **kwargs)
        self.response = HTTPFound(location=url)
        if end:
            raise EndController(self.response)

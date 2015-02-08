from pytest import fixture

from haplugin.sql.fixtures import BaseFixtures

from basket.auth.models import User
from basket.teams.models import Team
from basket.groups.models import Group
from basket.games.models import Game


class Fixtures(BaseFixtures):
    users = [
        {'name': 'Socek'},
        {'name': 'Darek'},
        {'name': 'Marek'},
    ]
    teams = [
        {'name': "Przyjaciele Szymon", 'hometown': "Tarnowskie Góry"},
        {'name': "KKS TG", 'hometown': "Tarnowskie Góry"},
        {'name': "Kutna Hora", 'hometown': 'Kutna Hora'},
        {'name': "Békéscsaba", 'hometown': "Békéscsaba"},
        {'name': "OLIMPIA BASKET BORUSZOWICE", 'hometown': "Boruszowice"},
        {'name': "Machina AG Rolbud", 'hometown': "Radzionków"},
        {'name': "Boguszów-Gorce", 'hometown': 'Boguszów-Gorce'},
        {'name': "Fit Your Life T.G", 'hometown': 'Tarnowskie Góry'},
        {'name': "TG Team", 'hometown': 'Tarnowskie Góry'},
        {
            'name': 'A.S. Basket HEF Lubliniec',
            'hometown': 'A.S. Basket HEF Lubliniec'
        },
    ]
    groups = [
        {'name': 'Grupa A'},
        {'name': 'Grupa B'},
        {'name': 'Finały'},
    ]

    def make_all(self):
        self.create_dict(User, self.users)
        self.create_dict(Team, self.teams)
        self.create_dict(Group, self.groups)
        self.create_games()

    def create_dict(self, cls, data):
        if 'name' in data[0]:
            create = self._create
        else:
            create = self._create_nameless

        for item in data:
            create(cls, **item)

    def create_games(self):
        self._create_game(
            index=0,
            left_team=self.fixtures['Team']['Przyjaciele Szymon'],
            right_team=self.fixtures['Team']['TG Team'],
        )

        self._create_game(
            index=1,
            left_team=self.fixtures['Team']['Kutna Hora'],
            right_team=self.fixtures['Team']['Machina AG Rolbud'],
        )

    def _create_game(self, **kwargs):
        obj = self._create_nameless(Game, **kwargs)
        obj.add_to_db_session(self.db)


@fixture(scope="session")
def fixtures(db, app):
    print("Creating fixtures...")
    return Fixtures(db, app).create_all()

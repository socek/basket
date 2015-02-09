from datetime import datetime
from pytest import fixture

from haplugin.sql.fixtures import BaseFixtures

from basket.auth.models import User
from basket.teams.models import Team
from basket.groups.models import Group
from basket.games.models import Game
from basket.place.models import Place


class Fixtures(BaseFixtures):
    users = [
        {
            'name': 'Socek',
            'email': 'msocek@gmail.com',
            'password': (
                '08d94068d7dd5f83ebb7b008250f904b188ba14ce41851bb779d92cf843db'
                '12cdd43a17b2db8aeb2'
            ),
        },
        {'name': 'Darek'},
        {'name': 'Marek'},
    ]
    T_PRZYJACIELE = "Przyjaciele Szymon"
    T_KKS = "KKS TG"
    T_KUTNA = "Kutna Hora"
    T_BEKESCABA = "Békéscsaba"
    T_OLIMPIA = "Olimpia Basket Boruszowice"
    T_MACHINA = "Machina AG Rolbud"
    T_BOGUSZOW = "Boguszów-Gorce"
    T_FIT = "Fit Your Life T.G"
    T_TGTEAM = "TG Team"
    T_LUBLINIEC = 'A.S. Basket HEF Lubliniec'
    teams = [
        {'name': T_PRZYJACIELE, 'hometown': "Tarnowskie Góry"},
        {'name': T_KKS, 'hometown': "Tarnowskie Góry"},
        {'name': T_KUTNA, 'hometown': 'Kutna Hora'},
        {'name': T_BEKESCABA, 'hometown': "Békéscsaba"},
        {'name': T_OLIMPIA, 'hometown': "Boruszowice"},
        {'name': T_MACHINA, 'hometown': "Radzionków"},
        {'name': T_BOGUSZOW, 'hometown': 'Boguszów-Gorce'},
        {'name': T_FIT, 'hometown': 'Tarnowskie Góry'},
        {'name': T_TGTEAM, 'hometown': 'Tarnowskie Góry'},
        {'name': T_LUBLINIEC, 'hometown': 'A.S. Basket HEF Lubliniec'},
    ]
    groups = [
        {'name': 'Grupa A'},
        {'name': 'Grupa B'},
        {'name': 'Finały'},
    ]

    P_TG = 'Hala Sportowa Tarnowskie Góry'
    P_RADZIONKOW = 'Hala MOSiR Radzionków'
    places = [
        {'name': P_TG},
        {'name': P_RADZIONKOW},
    ]

    def make_all(self):
        self.create_dict(User, self.users)
        self.create_dict(Team, self.teams)
        self.create_dict(Group, self.groups)
        self.create_dict(Place, self.places)
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
            left_team=self.fixtures['Team'][self.T_PRZYJACIELE],
            right_team=self.fixtures['Team'][self.T_KKS],
            date=datetime(2015, 3, 5, 17, 30),
            group=self.fixtures['Group']['Grupa A'],
            place=self.fixtures['Place'][self.P_TG],
        )

        self._create_game(
            index=1,
            left_team=self.fixtures['Team'][self.T_KUTNA],
            right_team=self.fixtures['Team'][self.T_BEKESCABA],
            date=datetime(2015, 3, 5, 19, 00),
            group=self.fixtures['Group']['Grupa A'],
            place=self.fixtures['Place'][self.P_TG],
        )

        self._create_game(
            index=2,
            left_team=self.fixtures['Team'][self.T_MACHINA],
            right_team=self.fixtures['Team'][self.T_TGTEAM],
            date=datetime(2015, 3, 5, 19, 00),
            group=self.fixtures['Group']['Grupa B'],
            place=self.fixtures['Place'][self.P_TG],
        )

        self._create_game(
            index=3,
            left_team=self.fixtures['Team'][self.T_PRZYJACIELE],
            right_team=self.fixtures['Team'][self.T_OLIMPIA],
            date=datetime(2015, 3, 6, 9, 30),
            group=self.fixtures['Group']['Grupa A'],
            place=self.fixtures['Place'][self.P_TG],
        )

        self._create_game(
            index=4,
            left_team=self.fixtures['Team'][self.T_KKS],
            right_team=self.fixtures['Team'][self.T_KUTNA],
            date=datetime(2015, 3, 6, 11, 00),
            group=self.fixtures['Group']['Grupa A'],
            place=self.fixtures['Place'][self.P_TG],
        )

        self._create_game(
            index=5,
            left_team=self.fixtures['Team'][self.T_BEKESCABA],
            right_team=self.fixtures['Team'][self.T_OLIMPIA],
            date=datetime(2015, 3, 6, 12, 30),
            group=self.fixtures['Group']['Grupa A'],
            place=self.fixtures['Place'][self.P_TG],
        )

        self._create_game(
            index=6,
            left_team=self.fixtures['Team'][self.T_KUTNA],
            right_team=self.fixtures['Team'][self.T_PRZYJACIELE],
            date=datetime(2015, 3, 6, 14, 00),
            group=self.fixtures['Group']['Grupa A'],
            place=self.fixtures['Place'][self.P_TG],
        )

        self._create_game(
            index=7,
            left_team=self.fixtures['Team'][self.T_KKS],
            right_team=self.fixtures['Team'][self.T_OLIMPIA],
            date=datetime(2015, 3, 6, 15, 30),
            group=self.fixtures['Group']['Grupa A'],
            place=self.fixtures['Place'][self.P_TG],
        )

        self._create_game(
            index=8,
            left_team=self.fixtures['Team'][self.T_BEKESCABA],
            right_team=self.fixtures['Team'][self.T_PRZYJACIELE],
            date=datetime(2015, 3, 6, 17, 00),
            group=self.fixtures['Group']['Grupa A'],
            place=self.fixtures['Place'][self.P_TG],
        )

        self._create_game(
            index=9,
            left_team=self.fixtures['Team'][self.T_OLIMPIA],
            right_team=self.fixtures['Team'][self.T_KUTNA],
            date=datetime(2015, 3, 6, 18, 30),
            group=self.fixtures['Group']['Grupa A'],
            place=self.fixtures['Place'][self.P_TG],
        )

        self._create_game(
            index=10,
            left_team=self.fixtures['Team'][self.T_KKS],
            right_team=self.fixtures['Team'][self.T_BEKESCABA],
            date=datetime(2015, 3, 6, 20, 00),
            group=self.fixtures['Group']['Grupa A'],
            place=self.fixtures['Place'][self.P_TG],
        )

        self._create_game(
            index=11,
            left_team=self.fixtures['Team'][self.T_MACHINA],
            right_team=self.fixtures['Team'][self.T_BOGUSZOW],
            date=datetime(2015, 3, 6, 8, 00),
            group=self.fixtures['Group']['Grupa B'],
            place=self.fixtures['Place'][self.P_RADZIONKOW],
        )

        self._create_game(
            index=12,
            left_team=self.fixtures['Team'][self.T_LUBLINIEC],
            right_team=self.fixtures['Team'][self.T_FIT],
            date=datetime(2015, 3, 6, 9, 30),
            group=self.fixtures['Group']['Grupa B'],
            place=self.fixtures['Place'][self.P_RADZIONKOW],
        )

        self._create_game(
            index=13,
            left_team=self.fixtures['Team'][self.T_BOGUSZOW],
            right_team=self.fixtures['Team'][self.T_TGTEAM],
            date=datetime(2015, 3, 6, 11, 00),
            group=self.fixtures['Group']['Grupa B'],
            place=self.fixtures['Place'][self.P_RADZIONKOW],
        )

        self._create_game(
            index=14,
            left_team=self.fixtures['Team'][self.T_MACHINA],
            right_team=self.fixtures['Team'][self.T_FIT],
            date=datetime(2015, 3, 6, 13, 00),
            group=self.fixtures['Group']['Grupa B'],
            place=self.fixtures['Place'][self.P_RADZIONKOW],
        )

        self._create_game(
            index=15,
            left_team=self.fixtures['Team'][self.T_TGTEAM],
            right_team=self.fixtures['Team'][self.T_LUBLINIEC],
            date=datetime(2015, 3, 6, 14, 30),
            group=self.fixtures['Group']['Grupa B'],
            place=self.fixtures['Place'][self.P_RADZIONKOW],
        )

        self._create_game(
            index=16,
            left_team=self.fixtures['Team'][self.T_BOGUSZOW],
            right_team=self.fixtures['Team'][self.T_FIT],
            date=datetime(2015, 3, 6, 16, 00),
            group=self.fixtures['Group']['Grupa B'],
            place=self.fixtures['Place'][self.P_RADZIONKOW],
        )

        self._create_game(
            index=17,
            left_team=self.fixtures['Team'][self.T_MACHINA],
            right_team=self.fixtures['Team'][self.T_LUBLINIEC],
            date=datetime(2015, 3, 6, 17, 30),
            group=self.fixtures['Group']['Grupa B'],
            place=self.fixtures['Place'][self.P_RADZIONKOW],
        )

        self._create_game(
            index=18,
            left_team=self.fixtures['Team'][self.T_FIT],
            right_team=self.fixtures['Team'][self.T_TGTEAM],
            date=datetime(2015, 3, 6, 19, 00),
            group=self.fixtures['Group']['Grupa B'],
            place=self.fixtures['Place'][self.P_RADZIONKOW],
        )

        self._create_game(
            index=19,
            left_team=self.fixtures['Team'][self.T_BOGUSZOW],
            right_team=self.fixtures['Team'][self.T_LUBLINIEC],
            date=datetime(2015, 3, 6, 20, 30),
            group=self.fixtures['Group']['Grupa B'],
            place=self.fixtures['Place'][self.P_RADZIONKOW],
        )

        self._create_game(
            index=20,
            date=datetime(2015, 3, 7, 10, 00),
            group=self.fixtures['Group']['Finały'],
            place=self.fixtures['Place'][self.P_TG],
        )

        self._create_game(
            index=21,
            date=datetime(2015, 3, 7, 12, 00),
            group=self.fixtures['Group']['Finały'],
            place=self.fixtures['Place'][self.P_TG],
        )

        self._create_game(
            index=22,
            date=datetime(2015, 3, 7, 15, 00),
            group=self.fixtures['Group']['Finały'],
            place=self.fixtures['Place'][self.P_TG],
        )

        self._create_game(
            index=23,
            date=datetime(2015, 3, 7, 16, 30),
            group=self.fixtures['Group']['Finały'],
            place=self.fixtures['Place'][self.P_TG],
        )

    def _create_game(self, **kwargs):
        obj = self._create_nameless(Game, **kwargs)
        obj.add_to_db_session(self.db)


@fixture(scope="session")
def fixtures(db, app):
    print("Creating fixtures...")
    return Fixtures(db, app).create_all()


def create_fixtures(registry):
    from basket.application.init import main
    db = registry['db']
    return Fixtures(db, main).create_all()

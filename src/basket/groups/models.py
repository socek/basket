from haplugin.sql import Base
from sqlalchemy import Column, Integer, String


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    info = Column(String)

    def generate_report(self):
        scores = {}
        for team in self._get_all_teams_from_games():
            scores[team.name] = {
                'name': team.name,
                'games': 0,
                'wins': 0,
                'score': 0,
                'small score': 0,
            }

        for report in self._get_active_games_reports():
            left, left_sum = self._get_score('left', scores, report)
            right, right_sum = self._get_score('right', scores, report)

            if left_sum > right_sum:
                self._submit_win(left)
            elif left_sum == right_sum:
                self._submit_draw(left)
                self._submit_draw(right)
            else:
                self._submit_win(right)

        return sorted(
            scores.values(),
            key=lambda row: (row['score'], row['small score']),
            reverse=True,
        )

    def _get_all_teams_from_games(self):
        teams = []
        for game in self.games:
            if game.left_team not in teams:
                teams.append(game.left_team)
                yield game.left_team
            if game.right_team not in teams:
                teams.append(game.right_team)
                yield game.right_team

    def _get_active_games_reports(self):
        for game in self.games:
            if game.status == 'ended':
                yield game.get_report()

    def _get_score(self, name, scores, report):
        data = scores[report[name]['team']]
        data['games'] += 1
        data['small score'] += report[name]['sum']
        return data, report[name]['sum']

    def _submit_win(self, score):
        score['wins'] += 1
        score['score'] += 2

    def _submit_draw(self, score):
        score['score'] += 1

from haplugin.jinja2 import Jinja2HelperSingle
from haplugin.formskit.helpers import FormWidget
from jinja2.exceptions import TemplateNotFound


def has_access_to_route(route):
    def decorator(method):
        def run_if_able(self, *args, **kwargs):
            if self.user.has_access_to_route(route):
                return method(self, *args, **kwargs)
            else:
                return ''
        return run_if_able
    return decorator


class GameWidget(Jinja2HelperSingle):

    template = 'basket.games:templates/game.haml'

    STATES = {
        'not started': 'Nie rozpoczęto',
        'running': 'W trakcie',
        'ended': 'Zakończony',
    }

    def __init__(self, request, game):
        super().__init__(request)
        self.game = game

    def make(self):
        self.data['game'] = self.game
        self.data['report'] = self.report = self.game.get_report()
        self.data['state'] = self.state
        self.data['group'] = self.group

    def state(self):
        data = {}
        if self.report['status'] == 'running':
            data['cls'] = ' red'
        elif self.report['status'] == 'ended':
            data['cls'] = ' grey'
        else:
            data['cls'] = ''

        data['state'] = self.STATES.get(self.report['status'])
        return '<div class="pub_date%(cls)s">%(state)s</div>' % data

    def group(self):
        data = {}
        if self.report['group_name'] == 'Grupa A':
            data['cls'] = 'grupa_a'
        elif self.report['group_name'] == 'Grupa B':
            data['cls'] = 'grupa_b'
        else:
            data['cls'] = 'finaly'

        data['group'] = self.report['group_name']
        return '<div class="tabel %(cls)s">%(group)s</div>' % data


class ScoreFormWidget(FormWidget):

    prefix = 'basket.games:templates/forms'

    def render_for(self, name, data):
        self.generate_data()
        self.data.update(data)
        try:
            return self.render(self.get_template(name, self.prefix))
        except TemplateNotFound:
            return self.render(self.get_template(name, super().prefix))

    def render(self, template_name):
        from jinja2 import Markup
        env = self.registry['jinja2']
        template = env.get_template(template_name)
        return Markup(template.render(**self.data))

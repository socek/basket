from haplugin.jinja2 import Jinja2HelperSingle

from .models import MenuObject


class MenuWidget(Jinja2HelperSingle):

    template = 'basket.menu:templates/main.jinja2'

    def __init__(self, request, highlighted):
        super().__init__(request)
        self.highlighted = highlighted

    def add_menu(self, *args, **kwargs):
        menu = MenuObject(self, *args, **kwargs)
        self.data['menu'].append(menu)
        return menu

    def make(self):
        self.data['menu'] = []
        submenu = self.add_menu('2015', None, 'calendar')
        submenu.add_child('Wszystkie', 'games:list', None)
        submenu.add_child('Grane', 'games:active_list', None)
        submenu.add_child('Grupa A', 'games:group_a', None)
        submenu.add_child('Grupa B', 'games:group_b', None)
        submenu.add_child('Finały', 'games:finals', None)
        # submenu.add_child('Konkursy', None, None)

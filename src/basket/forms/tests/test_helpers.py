from pytest import fixture, yield_fixture
from mock import MagicMock, patch

from hatak.testing import RequestFixture

from ..helpers import FormWidget


class TestsFormWidget(RequestFixture):

    @fixture
    def form(self):
        return MagicMock()

    @fixture
    def widget(self, request, form):
        return FormWidget(request, form)

    @yield_fixture
    def render_for(self, widget):
        with patch.object(widget, 'render_for', autospec=True) as mock:
            yield mock

    def test_combobox(self, request, widget, form, render_for):
        self._input_test(render_for, widget, form, 'combobox')

        request.add_js_link.assert_called_once_with('/js/combobox.js')
        request.add_js.assert_called_once_with(
            '''$(document).ready(function() {
                $("#%s").combobox();
                });''' % (widget.get_id('myname')))

    def _input_test(self, render_for, widget, form, name, method_name=None):
        method_name = method_name or name
        input_name = 'myname'

        method = getattr(widget, method_name)
        result = method(input_name, True, False)
        field = form.fields[name]

        self.assert_render_for(
            result,
            render_for,
            name + '.jinja2',
            {
                'name': field.get_name(),
                'value': form.get_value.return_value,
                'field': field,
                'id': '%s_myname' % (form.get_name()),
                'label': field.label,
                'error': field.error,
                'messages': (
                    form.fields.__getitem__.return_value
                    .get_error_messages.return_value
                ),
                'value_messages': (
                    form.fields.__getitem__.return_value
                    .get_value_errors.return_value
                ),
                'disabled': True,
                'autofocus': False,
            },)

    def assert_render_for(self, result, render_for, *args, **kwargs):
        assert result == render_for.return_value
        render_for.assert_called_once_with(*args, **kwargs)

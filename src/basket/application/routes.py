def make_routes(app, route):
    route.prefix = 'basket.'
    app.config.add_static_view(
        name='static',
        path=app.settings['paths:static'])
    route.read_yaml(app.settings['paths:routes'])

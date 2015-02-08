def make_settings(settings, paths):
    settings['db']['name'] = 'basket_test'
    settings['db']['testurl'] = (
        '%(type)s://%(login)s:%(password)s@%(host)s:%(port)s/postgres')

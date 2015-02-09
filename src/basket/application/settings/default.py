def make_settings(settings, paths):
    paths['data'] = 'data'

    settings['jinja2.directories'] = 'basket.application:templates'
    settings['debug'] = False
    settings['authentication_debug'] = False
    settings['session.type'] = 'file'
    settings['session.key'] = 'needtochangethis'
    settings['session.secret'] = 'needtochangethistoo'
    settings['session.cookie_on_exception'] = True

    paths['session'] = {
        'data_dir': ["%(data)s", 'sessions', 'data'],
        'lock_dir': ["%(data)s", 'sessions', 'lock'],
    }
    settings['session.data_dir'] = '%(paths:session:data_dir)s'
    settings['session.lock_dir'] = '%(paths:session:lock_dir)s'

    paths['frontend'] = ['%(data)s', 'frontend.ini']
    paths['logging'] = {
        'config': '%(frontend)s'
    }
    paths['static'] = 'basket.application:static'
    paths['routes'] = ['%(project_path)s', 'routes.yml']

    paths.set_path('sqlite_db', 'data', '%(db:name)s.db')
    settings['db'] = {}
    settings['db']['type'] = 'sqlite'
    settings['db']['name'] = 'basket_develop'
    # ----------------------------------------
    # This is example postgresql configuration
    # ----------------------------------------
    # settings['db']['type'] = 'postgresql'
    # settings['db']['login'] = 'develop'
    # settings['db']['password'] = 'develop'
    # settings['db']['host'] = 'localhost'
    # settings['db']['port'] = '5432'

    paths['alembic'] = {
        'versions': 'alembic',
        'ini': ['%(data)s', 'alembic.ini'],
    }

    settings['css'] = [
        '/css/bootstrap.min.css',
        '/css/plugins/metisMenu/metisMenu.min.css',
        '/css/plugins/timeline.css',
        '/css/sb-admin-2.css',
        '/css/plugins/morris.css',
        '/font-awesome-4.1.0/css/font-awesome.min.css',
        '/css/jquery-ui.min.css',
        '/css/jquery-ui.structure.min.css',
        '/css/jquery-ui.theme.min.css',
    ]

    settings['js'] = [
        '/js/jquery-1.11.0.js',
        '/js/bootstrap.min.js',
        '/js/plugins/metisMenu/metisMenu.min.js',
        '/js/jquery-ui.min.js',
        '/js/sb-admin-2.js',
    ]

    settings['auth_redirect'] = 'games:list'

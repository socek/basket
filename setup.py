# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'hatak==0.2.7',
    'coverage',
    'hatak_logging',
    'hatak_jinja2',
    'hatak_haml',
    'hatak_sql>=0.1.6',
    'hatak_alembic',
    'hatak_beaker',
    'hatak_debugtoolbar',
    'hatak_statics',
    'waitress',
    'uwsgi',
    'pytest',
    'pytest-cov',
    'coverage==3.7.1',
]
dependency_links = [

]

if __name__ == '__main__':
    setup(name='Basket',
          version='0.1',
          packages=find_packages('src'),
          package_dir={'': 'src'},
          install_requires=install_requires,
          dependency_links=dependency_links,
          include_package_data=True,
          entry_points="""\
            [paste.app_factory]
                main = basket.application.init:main
            [console_scripts]
                basket_manage = basket.application.manage:run
          """,
          )

# -*- coding:utf-8 -*-

import os
from setuptools import setup, find_packages

version = '1.0dev0'
long_description = open("README.txt").read() + "\n" + \
                   open(os.path.join("docs", "INSTALL.txt")).read() + "\n" + \
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" + \
                   open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='collective.varnish.webgui',
      version=version,
      description="Is tool that can be used to administer and monitor your Varnish servers.",
      long_description=long_description,
      classifiers=[
        "Framework :: Flask",
        "Framework :: Bootstrap",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: Varnish",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='python javascript flask bootstrap',
      author='Cleber J Santos',
      author_email='cleber@cleberjsantos.com.br',
      url='http://github.com/cleberjsantos/collective.varnish.webgui',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective', 'collective.varnish'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'Flask',
        'Flask-Bootstrap',
        'Werkzeug',
        'Flask-GoogleLogin',
        'Flask-Security',
        'Flask-Auth',
        'Flask-OAuth',
        'SQLAlchemy',
        'psycopg2',
        'Flask-SQLAlchemy',
        'Flask-Gravatar',
        'Flask-Cache',
        'Flask-Environments',
        'python-varnish',
        'PyMunin',
        ],
      extras_require={
        'test': [
            'Flask-Testing',
            'robotsuite',
            'robotframework-selenium2library',
        ],
      },
      entry_points="""\
      [console_scripts]
      varnishwebguictl = collective.varnish.webgui.webguiserver:run

      [paste.app_factory]
      main = collective.varnish.webgui.webguiserver:make_app
      debug = collective.varnish.webgui.webguiserver:make_debug

      [z3c.autoinclude.plugin]
      target = collective.varnish.webgui
      """,
      )

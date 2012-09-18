# -*- coding:utf-8 -*-

import os
from setuptools import setup, find_packages

version = '1.0dev0'
long_description = open("README.txt").read() + "\n" + \
                   open(os.path.join("docs", "INSTALL.txt")).read() + "\n" + \
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" + \
                   open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='colllective.varnish.webgui',
      version=version,
      description="Is tool that can be used to administer and monitor your Varnish servers.",
      long_description=long_description,
      classifiers=[
        "Framework :: Pyramid",
        "Framework :: Bootstrap",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='python javascript pyramid bootstrap pylons',
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
        'pyramid>=1.3',
        'pyramid_chameleon_genshi==0.6',
        'pyramid_command==0.1',
        'pyramid_debugtoolbar==1.0.2',
        'deform_bootstrap',
        'pyramid_oauth2_client',
        'pyramid_rewrite==0.2',
        'pyramid_xmlrpc',
        'sqlalchemy',
        'python-varnish',
        ],
      paster_plugins=['pyramid'],
      entry_points="""\
      [paste.app_factory]
      main = collective.varnish.webgui:main

      [z3c.autoinclude.plugin]
      target = collective.varnish.webgui
      """,
      )

# -*- coding: utf-8 -*-
"""Startup utilities"""
import os
import sys
from functools import partial
from pkg_resources import resource_filename

from flask import Flask, request

import paste.script.command
import werkzeug.script
import logging

prognameexec = sys.argv[0]
progname = str(sys.argv[0].split('/')[-1])
stderr = sys.stderr
stdout = sys.stdout
exit = sys.exit
__base = os.getcwd()


def usage(msg):
    """Print a brief error message to stderr and exit(2)."""
    stderr.write("Error: %s\n" % str(msg))
    stderr.write("For help, use %s -h\n" % prognameexec)
    exit(2)


def default_configfile(pathdir, filename):
    """ Return the name of the found config file or raise. """
    base = __base
    paths = []
    pathdir = os.path.join(base, pathdir)
    config = None

    if os.path.exists(pathdir):
        if filename in os.listdir(pathdir):
            paths.append(os.path.join(__base, pathdir, filename))
            config = paths[0]
        else:
            # Default configuration files
            paths.append(resource_filename(__name__, 'skel/' + filename))
            config = paths[0]
    else:
        # Default configuration files
        paths.append(resource_filename(__name__, 'skel/' + filename))
        config = paths[0]
    sys.path[0:0] = paths
    if config is None:
        usage('No config file found at default paths (%s); '
              'use the -c option to specify a config file '
              'at a different path' % ', '.join(paths))
    return config

_buildout_path = partial(os.path.join, default_configfile)
abspath = _buildout_path()
DEPLOY_INI = abspath('etc', 'deploy.ini')
DEPLOY_CFG = abspath('etc', 'deploy.cfg')


del _buildout_path


def log(msg, logfile):
    """ Create logfile """
    logger = logging.getLogger(progname)
    hdlr = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    return logger


# bin/paster serve parts/etc/deploy.ini
def make_app(global_conf={}, config=DEPLOY_CFG):
    from collective.varnish.webgui import app
    app.config.from_pyfile(config)
    if app.debug:
        print '\n\nInitialized: DEBUG MODE\n\n'
        from werkzeug.debug import DebuggedApplication
        return DebuggedApplication(app, evalex=True)
    else:
        return app


# bin/varnishwebguictl shell
def make_shell():
    """Interactive VarnishWebGui Shell"""
    from collective.varnish.webgui import init_db as initdb
    app = make_app()
    http = app.test_client()
    reqctx = app.test_request_context
    return locals()


def _init_db(debug=False, dry_run=False):
    """Initialize the database."""
    from collective.varnish.webgui import init_db
    print 'init_db()'
    if dry_run:
        return
    make_app()
    # Create the tables
    init_db()


def _serve(action, debug=False, dry_run=False):
    """Build paster command from 'action' and 'debug' flag."""
    if action == 'initdb':
        # First, create the tables
        return _init_db(debug=debug, dry_run=dry_run)
    config = DEPLOY_INI
    argv = ['bin/paster', 'serve', config]
    if action in ('start', 'restart'):
        argv += [action, '--daemon']
    elif action in ('', 'fg', 'foreground'):
        argv += ['--reload']
    else:
        argv += [action]
    # Print the 'paster' command
    print ' '.join(argv)
    if dry_run:
        return
    # Configure logging and lock file
    if action in ('start', 'stop', 'restart', 'status'):
        log_pathdir = os.path.join(__base, 'var/log/')
        pid_pathdir = os.path.join(__base, 'var/')

        if not 'varnishwebgui.log' in os.listdir(log_pathdir):
            log('Starting server', log_pathdir + 'varnishwebgui.log')
            log_file = abspath('var/log', 'varnishwebgui.log')
        else:
            log_file = abspath('var/log', 'varnishwebgui.log')

        if not 'varnishwebgui.pid' in os.listdir(pid_pathdir):
            file(str(pid_pathdir + 'varnishwebgui.pid'), 'w').write('')
            pid_file = abspath('var', 'varnishwebgui.pid')
        else:
            pid_file = abspath('var', 'varnishwebgui.pid')

        argv += [
            '--log-file', log_file,
            '--pid-file', pid_file,
        ]
    sys.argv = argv[:2] + [config] + argv[3:]
    # Run the 'paster' command
    paste.script.command.run()


# bin/varnishwebguictl ...
def run():
    action_shell = werkzeug.script.make_shell(make_shell, make_shell.__doc__)

    # bin/varnishwebguictl serve [fg|start|stop|restart|status|initdb]
    def action_serve(action=('a', 'start'), dry_run=False):
        """Serve the application.

        This command serves a web application that uses a paste.deploy
        configuration file for the server and application.

        Options:
         - 'action' is one of [fg|start|stop|restart|status|initdb]
         - '--dry-run' print the paster command and exit
        """
        _serve(action, debug=False, dry_run=dry_run)

    # bin/varnishwebguictl debug [fg|start|stop|restart|status|initdb]
    def action_debug(action=('a', 'start'), dry_run=False):
        """Serve the debugging application."""
        _serve(action, debug=True, dry_run=dry_run)

    # bin/varnishwebguictl status
    def action_status(dry_run=False):
        """Status of the application."""
        _serve('status', dry_run=dry_run)

    # bin/varnishwebguictl stop
    def action_stop(dry_run=False):
        """Stop the application."""
        _serve('stop', dry_run=dry_run)

    werkzeug.script.run()

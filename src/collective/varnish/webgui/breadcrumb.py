# -*- coding: UTF-8 -*-
import functools
import collections

import flask

BreadCrumb = collections.namedtuple('BreadCrumb', ['path', 'title'])


def breadcrumb(view_title):
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            # Put title into flask.g so views have access and
            # don't need to repeat it
            flask.g.title = view_title
            # Also put previous breadcrumbs there, ready for view to use
            session_crumbs = flask.session.setdefault('crumbs', [])
            flask.g.breadcrumbs = []
            for path, title in session_crumbs:
                flask.g.breadcrumbs.append(BreadCrumb(path, title))

            # Call the view
            rv = f(*args, **kwargs)

            # Now add the request path and title for that view
            # to the list of crumbs we store in the session.
            flask.session.modified = True
            session_crumbs.append((flask.request.path, view_title))
            # Only keep most recent crumbs (number should be configurable)
            if len(session_crumbs) > 3:
                session_crumbs.pop(0)

            return rv
        return decorated_function
    return decorator

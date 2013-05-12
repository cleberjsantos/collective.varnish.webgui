# -*- coding: UTF-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from collective.varnish.webgui import app


SQLALCHEMY_DATABASE = app.config.get('SQLALCHEMY_DATABASE_URI', 'sqlite:////tmp/app.db')
SQLALCHEMY_UNICODE = app.config.get('SQLALCHEMY_NATIVE_UNICODE', True)

engine = create_engine(SQLALCHEMY_DATABASE, convert_unicode=SQLALCHEMY_UNICODE)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

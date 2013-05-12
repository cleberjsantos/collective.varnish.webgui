# -*- coding: utf-8 -*-
"""
Module to provide plug-and-play authentication support for SQLAlchemy.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy import Sequence

from database import Base
import datetime

from flaskext.auth import AuthUser, get_current_user_data

from collective.varnish.webgui import app
from collective.varnish.webgui import db


def get_user_class(declarative_base):
    """
    Factory function to create an SQLAlchemy User model with a declarative base
    """
    class User(declarative_base, AuthUser):
        """
        Implementation of User for SQLAlchemy.
        """
        id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
        username = Column(String(80), nullable=False, unique=True)
        first_name = Column(String(50), nullable=True)
        last_name = Column(String(50), nullable=True)
        salt = Column(String(80))
        password = Column(String(120), nullable=False)
        role = Column(String(80), nullable=True)
        created = Column(DateTime(), default=datetime.datetime.utcnow)
        modified = Column(DateTime(), default=datetime.datetime.utcnow)
        admincreated = Column(Boolean, default=False, unique=False)

        def __init__(self, *args, **kwargs):
            super(User, self).__init__(*args, **kwargs)
            self.username = kwargs.get('username')
            self.password = kwargs.get('password')
            self.first_name = kwargs.get('first_name')
            self.last_name = kwargs.get('last_name')
            self.created = kwargs.get('created')
            if self.password is not None and not self.id:
                # Initialize and encrypt password before first save.
                self.set_and_encrypt_password(self.password)
                self.admincreated = True
                self.role = 'administrador'

        def __getstate__(self):
            return {
                'id': self.id,
                'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'role': self.role,
                'created': self.created,
                'modified': self.modified,
                'admincreated': self.admincreated
            }

        @classmethod
        def load_current_user(cls, apply_timeout=True):
            data = get_current_user_data(apply_timeout)
            if not data:
                return None
            return cls.query.filter(cls.username == data['username']).one()

    return User

# -*- coding: utf-8 -*-
import random
import string

from webguiserver import DEPLOY_INI, DEPLOY_CFG

from flask import Flask, request, render_template, flash, redirect,\
                    url_for, session, g, make_response
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form, TextField, HiddenField, ValidationError,\
                                  Required, RecaptchaField, PasswordField

from flask.ext.auth import Auth, AuthUser, login_required, logout
from flask.ext.sqlalchemy import SQLAlchemy

from flaskext.gravatar import Gravatar
from flask.ext.cache import Cache

from sqlalchemy.sql import select, and_

app = Flask(__name__)
Bootstrap(app)
cache = Cache(app)

# Gravatar default parameters
gravatar = Gravatar(app,
                    size=27,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False)


class _DefaultSettings(object):
    """ Loaded environment variables
        through configuration file through database
    """
    CSRF_ENABLED = app.config.get('CSRF_ENABLED', False)
    # Random unique secrete key
    SECRET_KEY = str("".join( [random.choice(string.letters) for i in xrange(15)] ) + "".join( [random.choice(string.digits) for i in xrange(8)] ))
    CACHE_TYPE = app.config.get('CACHE_TYPE', 'simple')
    app.config.from_pyfile(DEPLOY_CFG)

app.config.from_object(_DefaultSettings)
del _DefaultSettings

# Instantiate DB
db = SQLAlchemy(app)

from models.appmodels import get_user_class
from models.database import db_session, engine


## Set SQL Alchemy to automatically tear down
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

# Instantiate authentication
auth = Auth(app, login_url_name='login')
User = get_user_class(db.Model)


class LoginForm(Form):
    username = TextField('Username',
                        description='Enter your email.',
                        validators=[Required()]
               )

    password = PasswordField('Password',
                            description='Enter your password.',
                            validators=[Required()]
               )

    recaptcha = RecaptchaField()


def index():
    return render_template('index.html', page_name="index")


def about():
    return render_template('about.html', page_name="about")

##login methods


@login_required()
def home():
    ##Dump variables in templates
    return render_template('home.html', page_name="home")


def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter(User.username == username).first()
        if user is not None:
            # Authenticate and log in!
            if user.authenticate(request.form['password']):
                session['username'] = request.form['username']
                return redirect(url_for('home'))
            else:
                flash('Incorrect password. Please try again')
                return render_template('login.html', form=form, page_name="login")
        else:
            flash('Incorrect username. Please try again')
            return render_template('login.html', form=form, page_name="login")
    return render_template('login.html', form=form, page_name="login")


def user_create():
    if request.method == 'POST':
        username = request.form['username']
        if User.query.filter(User.username == username).first():
            return 'User already exists.'
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('user_create.html', page_name='createuser')


def logout_view():
    # remove the username from the session if it's there
    user_data = logout()
    session.pop('username', None)
    flash('Logged out user {0}.'.format(user_data['username']))
    return redirect(url_for('login'))


#@app.before_request
#def before_request():
#    g.db = engine.connect()
#    selecting_user = select([User], and_(User.admincreated == True, User.role == 'administrador'))
#    results = g.db.execute(selecting_user)
#    rows = results.fetchall()
#    results.close()
#    if len(rows) <= 0:
#        return render_template('user_create.html', page_name='createuser')

db.create_all()
conn = engine.connect()
selecting_user = select([User], and_(User.admincreated == True, User.role == 'administrador'))
results = conn.execute(selecting_user)
rows = results.fetchall()

results.close()

if len(rows) > 0:
    for row in rows:
        if row['admincreated'] == True and row['role'] == 'admin':
            app.add_url_rule('/users/create/', 'user_create', login, methods=['GET', 'POST'])
        else:
            app.add_url_rule('/users/create/', 'user_create', user_create, methods=['GET', 'POST'])
else:
    app.add_url_rule('/users/create/', 'user_create', user_create, methods=['GET', 'POST'])

# URLs
app.add_url_rule('/', 'index', index)
app.add_url_rule('/about/', 'about', about)
app.add_url_rule('/contact/', 'contact', about)
app.add_url_rule('/login/', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/home/', 'home', home)
app.add_url_rule('/logout/', 'logout', logout_view)

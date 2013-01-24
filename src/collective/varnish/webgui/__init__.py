# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form, TextField, HiddenField, ValidationError,\
                                  Required, RecaptchaField


class _DefaultSettings(object):
    BOOTSTRAP_USE_MINIFIED = True
    BOOTSTRAP_USE_CDN = True
    BOOTSTRAP_FONTAWESOME = True
    RECAPTCHA_PUBLIC_KEY = '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

app = Flask(__name__)
Bootstrap(app)

app.config.from_object(_DefaultSettings)
del _DefaultSettings


def init_db():
    """Create the database tables."""
    pass


#@app.route('/')
#def index():
#    if request.args:
#        BREAK(with_NameError)
#    import pdb; pdb.set_trace()
#    return 'Hello %s!' % app.config['USERNAME'].title()


class ExampleForm(Form):
    field1 = TextField('First Field', description='This is field one.')
    field2 = TextField('Second Field', description='This is field two.',
                       validators=[Required()])
    field3 = TextField('BIRO', description='TESTE LERO')
    hidden_field = HiddenField('You cannot see this', description='Nope')
    recaptcha = RecaptchaField('A sample recaptcha field')

    def validate_hidden_field(form, field):
        raise ValidationError('Always wrong')


@app.route('/', methods=('GET', 'POST',))
def index():
    form = ExampleForm()
    if form.validate_on_submit():
        return "PASSED"
    return render_template('example.html', form=form)


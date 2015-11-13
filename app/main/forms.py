from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required

class LoginForm(Form):
    id_no = StringField('ID No.', validators=[Required()])
    submit = SubmitField('Submit')


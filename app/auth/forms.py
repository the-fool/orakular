from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, RadioField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required

class LoginForm(Form):
    name = StringField('Name', validators=[Required()])
    id = IntegerField('ID', validators=[Required()])
    role = RadioField('Role', validators=[Required()],
                      choices=[('student','Student'),
                               ('faculty','Faculty'),
                               ('staff','Staff')])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')
    

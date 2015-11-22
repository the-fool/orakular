from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, RadioField, SelectField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, StopValidation, ValidationError, Length


                                        
class LoginForm(Form):
    id = IntegerField('ID', validators=[Required()])
    role = RadioField('Role', validators=[Required()],
                      choices=[('student','Student'),
                               ('faculty','Faculty'),
                               ('staff','Staff')])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')
    
class AddCourseForm(Form):
    cid = StringField('CID', validators=[Required()])
    cname = StringField('Course Name', validators=[Required()])
    faculty = SelectField('Faculty')
    submit = SubmitField('Add course')

from flask.ext.wtf import Form
from wtforms import SubmitField
from wtforms.validators import Required

class RegisterClassForm(Form):
    cid = HiddenField('cid')
    submit = SubmitField('Register', validators=[Required()])
    

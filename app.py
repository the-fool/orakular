from flask import Flask, render_template, session, redirect, url_for, request
import cx_Oracle
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required

from config import DBNAME, DBPASSWORD, DBADDRESS, SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap(app)

class LoginForm(Form):
    id_no = StringField('ID please', validators=[Required()])
    submit = SubmitField('Submit')


@app.route("/data/")
def hello():
	db = cx_Oracle.connect(DBNAME, DBPASSWORD, DBADDRESS)
	c = db.cursor()
	c.execute("select * from test")
	r = c.fetchall()
	s = ""
	for tup in r:
	  s += str(tup)
	return "here is your data: " + s


@app.route("/", methods=['GET', 'POST'])
def index():
    form = LoginForm()       
    if form.validate_on_submit():
       session['id_no'] = form.id_no.data
       return redirect(url_for('student'))
    return render_template("index.html", form=form, id_no=session.get('id_no'))

@app.route("/student")
def student():
    return render_template("student.html", id_no=session.get('id_no')) 

@app.route("/staff", methods=['GET', 'POST'])
def faculty():
    return render_template("faculty.html", id_no=session.get('id_no'))

if __name__ == '__main__':
	app.run(debug=True)

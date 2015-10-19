from flask import Flask, render_template, session, redirect, url_for, request, jsonify, flash
import cx_Oracle
from flask.ext.bootstrap import Bootstrap
from database import db_session
from models import Student, Faculty, Course, Department, Enrolled, Staff
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


@app.route("/", methods=['GET', 'POST'])
def index():
    form = LoginForm()       
    if form.validate_on_submit():
       session['id_no'] = form.id_no.data
       if session.get('id_no') is not None:
           flash('hello member')
       return redirect(url_for('index'))
    return render_template("index.html", form=form, id_no=session.get('id_no'))


@app.route("/student")
def student():
    return render_template("student.html", id_no=session.get('id_no')) 


@app.route("/staff", methods=['GET', 'POST'])
def staff():
    db = cx_Oracle.connect(DBNAME, DBPASSWORD, DBADDRESS)
    c = db.cursor()
    c.execute("select * from students")
    students = c.fetchall()
    return render_template("staff.html",  students=students, id_no=session.get('id_no'))


@app.route("/api/students")
def api_students():
    db = cx_Oracle.connect(DBNAME, DBPASSWORD, DBADDRESS)
    c = db.cursor()
    c.execute("select * from students")
    students = c.fetchall()
    keys = ['sid','sname','major','s_level','age']
    l = [dict(zip(keys, list(s))) for s in students]
    d = {'students': l}      
    return jsonify(d) 


if __name__ == '__main__':
	app.run(debug=True)

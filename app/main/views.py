from flask import render_template, session, redirect, url_for, request, jsonify, flash, current_app
from . import main
from ..student import student
import cx_Oracle
from ..database import db_session, cursor as c
from ..models import Student, Faculty, Course, Department, Enrolled, Staff
from forms import LoginForm

@main.route("/", methods=['GET', 'POST'])
def index():
    form = LoginForm()       
    if form.validate_on_submit():
       session['id_no'] = form.id_no.data
       if session.get('id_no') is not None:
           flash('hello member')
       return redirect(url_for('.index'))
    return render_template('index.html', 
                           form=form, 
			   id_no=session.get('id_no'))

@main.route("/dashboard")
def dash():
    return redirect(url_for("student.dashboard"))


@main.route("/courses")
def courses():
    courses = db_session.query(Course).all()
    return render_template("courses.html", courses=courses) 

@main.route("/staff", methods=['GET', 'POST'])
def staff():
    c.execute("select * from students")
    students = c.fetchall()
    return render_template("staff.html",  students=students, id_no=session.get('id_no'))

@main.route("/departments")
def departments():
    return "departments"

@main.route("/api/<target>")
def api(target):
    t = globals()[target.title()]
    l = table_to_dict(db_session.query(t).all())
    return jsonify({target: l})

def table_to_dict(table):
    l = []
    for row in table:
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        l.append(d)
    return l


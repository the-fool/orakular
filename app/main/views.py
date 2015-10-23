from flask import render_template, session, redirect, url_for, request, jsonify, flash
from . import main
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

@main.route("/student")
def student():
    return render_template("student.html", id_no=session.get('id_no')) 

@main.route("/staff", methods=['GET', 'POST'])
def staff():
    c.execute("select * from students")
    students = c.fetchall()
    return render_template("staff.html",  students=students, id_no=session.get('id_no'))


@main.route("/api/faculty")
def api_faculty():
    f_list = table_to_dict(db_session.query(Faculty).all())
    return jsonify({'faculty': f_list})
@main.route("/api/students")
def api_students():
    s_list = table_to_dict(db_session.query(Student).all())
    return jsonify({'student': s_list})
@main.route("/api/staff")
def api_staff():
    s_list = table_to_dict(db_session.query(Staff).all())
    return jsonify({'Staff': s_list})

def table_to_dict(table):
    l = []
    for row in table:
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        l.append(d)
    return l

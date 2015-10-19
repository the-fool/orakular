from flask import render_template, session, redirect, url_for, request, jsonify, flash
from . import main
import cx_Oracle
from ..database import db_session
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
    return render_template("main/index.html", form=form, id_no=session.get('id_no'))


@main.route("/student")
def student():
    return render_template("student.html", id_no=session.get('id_no')) 


@main.route("/staff", methods=['GET', 'POST'])
def staff():
    db = cx_Oracle.connect(DBNAME, DBPASSWORD, DBADDRESS)
    c = db.cursor()
    c.execute("select * from students")
    students = c.fetchall()
    return render_template("staff.html",  students=students, id_no=session.get('id_no'))


@main.route("/api/students")
def api_students():
    db = cx_Oracle.connect(DBNAME, DBPASSWORD, DBADDRESS)
    c = db.cursor()
    c.execute("select * from students")
    students = c.fetchall()
    keys = ['sid','sname','major','s_level','age']
    l = [dict(zip(keys, list(s))) for s in students]
    d = {'students': l}      
    return jsonify(d) 

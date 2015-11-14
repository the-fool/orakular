from flask import render_template, session, redirect, url_for, request, jsonify, flash, current_app
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import main
from ..student import student
import cx_Oracle
from ..database import db_session as sess
from ..models import Student, Faculty, Course, Department, Enrolled, Staff, User
from ..auth.forms import LoginForm
from ..decorators import non_student_only

@main.route("/", methods=['GET', 'POST'])
def index():
    form = LoginForm()       
    if form.validate_on_submit():
       user = User.check_user(id=form.id.data)
       if user is not None:
           login_user(user, form.remember_me.data)
           flash('hello member')
       else:
           flash('invalid id')
    if current_user.is_authenticated:
       return redirect(url_for('{0}.dashboard'.format(current_user.role)))
    else: 
        return render_template('index.html', 
                           form=form, 
			   id_no=session.get('id_no'))

@main.route("/courses")
def courses():
    if current_user.is_authenticated:
        if current_user.role == 'student':
            return redirect(url_for('student.courses'))

    course_list = session.query(Course).all()    
    return render_template("courses.html", form=None,
                           courses=course_list) 

@main.route("/departments")
def departments():
    return "departments"


@main.route("/ajax/student_modal")
@login_required
@non_student_only
def gen_student_modal():
    sid = request.args.get('sid','')
    try:
        student = 
            
    else:
        return "System error retrieving data."

@main.route("/api/<target>")
def api(target):
    t = globals()[target.title()]
    l = table_to_dict(session.query(t).all())
    return jsonify({target: l})

def table_to_dict(table):
    l = []
    for row in table:
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        l.append(d)
    return l


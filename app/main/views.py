from flask import render_template, session, redirect, url_for, request, jsonify, flash, current_app
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import main
from ..student import student
import cx_Oracle
from ..database import db_session as sess
from ..models import Student, Faculty, Course, Department, Enrolled, Staff, User
from ..auth.forms import LoginForm
from ..decorators import non_student_only
import cx_Oracle

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

    course_list = sess.query(Course).all()    
    return render_template("courses.html", form=None,
                           courses=course_list) 


@main.route("/ajax/student_modal")
@login_required
@non_student_only
def gen_student_modal():
    sid = request.args.get('sid','')
    try:
        student = sess.query(Student).filter_by(sid=sid).one()
        enrolled = sess.query(Enrolled).filter_by(sid=sid).all()
        e_list = [ {'c':sess.query(Course).filter_by(cid=x.cid).one(), 
                    'e':x} 
                   for x in enrolled]

        return render_template('student_modal_gen.html', 
                               s=student, e_list=e_list)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print "DB Error: {0} -- {1}".format(error.code, error.message)
        raise
    
@main.route("/dep")
def departments():
    return "filler"

@main.route("/dep/<int:did>")
def department_home(did):
    try:
        dep = sess.query(Department).filter_by(did=did).one()
        f_list = sess.query(Faculty).filter_by(deptid=did).all()
        s_list = sess.query(Staff).filter_by(deptid=did).all()
        c_list = []
        for c in sess.query(Course).all():
            if c.fid in [f.fid for f in f_list]:  # O(n^2)
                c_list.append(c)
        return render_template('department_home.html', dep=dep, 
                               f_list=f_list, c_list=c_list, s_list=s_list)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print "DB Error: {0} -- {1}".format(error.code, error.message)
        raise
    

@main.route("/api/<target>")
def api(target):
    t = globals()[target.title()]
    l = table_to_dict(sess.query(t).all())
    return jsonify({target: l})


def table_to_dict(table):
    l = []
    for row in table:
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        l.append(d)
    return l


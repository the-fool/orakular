from flask import render_template, url_for, redirect, request, flash, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import student
from ..models import User, Student, Enrolled, Course, Faculty
from .forms import RegisterClassForm
from ..database import db_session as sess
from ..decorators import student_only

@student.route('/dashboard', methods=['GET', 'POST'])
@login_required
@student_only
def dashboard():
    try:
        s = sess.query(Student).filter_by(sid=current_user.id).one()
        e = sess.query(Enrolled).filter_by(sid=s.sid).all()
        c = []
        grades = {}
        for x in e:
          cobj = sess.query(Course).filter_by(cid=x.cid).one()
          fobj = sess.query(Faculty).filter_by(fid=cobj.fid).one()
          c.append({'cobj':cobj, 'fobj':fobj})
          grades[x.cid] = x
    except:
        raise
    
    return render_template('student/dashboard.html', student=s, 
                           grades=grades, enrollment=e, courses=c)

@student.route('/courses/', methods=['GET', 'POST'])
@login_required
@student_only
def courses():
    form = RegisterClassForm()
    if form.validate_on_submit():
        
    course_list = sess.query(Course).all()
    enrolled = sess.query(Enrolled).filter(Enrolled.sid==current_user.id).all()
    e_list = []
    if enrolled is not None:
        e_list = [e.cid for e in enrolled]
    return render_template('courses.html', courses=course_list, enrolled=e_list)



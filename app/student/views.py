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
        current_user.courses = sess.query(Enrolled).filter_by(sid=s.sid).all()
        c = []
        grades = {}
        for x in current_user.courses:
          cobj = sess.query(Course).filter_by(cid=x.cid).one()
          fobj = sess.query(Faculty).filter_by(fid=cobj.fid).one()
          c.append({'cobj':cobj, 'fobj':fobj})
          grades[x.cid] = x
    except:
        raise
    
    return render_template('student/dashboard.html', student=s, 
                           grades=grades, courses=c)

@student.route('/courses/', methods=['GET', 'POST'])
@login_required
@student_only
def courses():
    if current_user.courses is None:
        current_user.courses = sess.query(Enrolled).filter_by(sid=current_user.id)
    
    form = RegisterClassForm()
    if form.validate_on_submit():
        if register_course(form.cid.data):
            flash('registered')
        return redirect(url_for('.courses'))

    course_list = sess.query(Course).all()
    e_list = []
    if current_user.courses is not None:
        e_list = [e.cid for e in current_user.courses]

    return render_template('courses.html', form=form,
                           courses=course_list, enrolled=e_list)


def register_course(cid):
    to_reg = sess.query(Course).filter_by(cid=cid).one()
    to_reg_sched = parse_time(to_reg)
    print to_reg_sched
    return True
    
def parse_time(course):
    schedule = {}
    meets = course.meets_at
    t = meets.split()[0].upper()
    h = [float(x.replace(':', '.')) for x in meets.split()[1].split('-')]
    days = ['M', 'TU', 'W', 'TH', 'F']
    for d in days:
        if t.find(d) != -1:
            schedule[d] = h
    return schedule



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
    current_user.courses = sess.query(Enrolled).filter_by(sid=current_user.id).all()

    form = RegisterClassForm()
    if form.validate_on_submit():
        if register_course(form.cid.data):
            flash('registered')
        else:
            flash('schedule conflict')
        return redirect(url_for('.courses'))

    course_list = sess.query(Course).all()
    e_list = []
    if current_user.courses:
        e_list = [e.cid for e in current_user.courses]

    return render_template('courses.html', form=form,
                           courses=course_list, enrolled=e_list)


def register_course(cid, sid=None):
    """sid param only set when this method is used as a util for db init """
    to_reg = sess.query(Course).filter_by(cid=cid).one()
    q = parse_time(to_reg)
    
    current_sched = [] 
    if sid is None: # default setting
        for x in current_user.courses:
            current_sched.append(parse_time(sess.query(Course).filter_by(cid=x.cid).one()))
    else:
        elist = sess.query(Enrolled).filter_by(sid=sid).all()
        for x in elist:
            current_sched.append(parse_time(sess.query(Course).filter_by(cid=x.cid).one()))

    for x in current_sched:
        for k in x.keys():
            if k in q:
                if ((max(x[k]) >= min(q[k]) >= min(x[k])) | 
                    (max(x[k]) >= max(q[k]) >= min(x[k])) |
                    (min(q[k]) <= min(x[k]) and max(q[k]) >= max(x[k]))):
                     return False
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



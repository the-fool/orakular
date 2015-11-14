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
        conf = check_schedule(form.cid.data)
        if conf == 0:
            enroll_course(form.cid.data)
            flash('You are registered for {0}.'.format(form.cid.data))
        else:
            flash('Schedule conflict with {0}.'.format(conf.cid))
        return redirect(url_for('.courses'))

    course_list = sess.query(Course).all()
    e_list = []
    if current_user.courses:
        e_list = [e.cid for e in current_user.courses]

    return render_template('courses.html', form=form,
                           courses=course_list, enrolled=e_list)


def check_schedule(cid, sid=None):
    """ sid param only set when this method is used as a util for db init 
    Returns 0 on no-conflict, otherwise the conflicting Enrolled Object  
    """
    to_reg = sess.query(Course).filter_by(cid=cid).one()
    q = parse_time(to_reg)
    
    current_sched = [] 
    if sid is None: # default setting
        for x in current_user.courses:
            current_sched.append( (parse_time(sess.query(Course).filter_by(cid=x.cid).one()), x) )
    
    else: # only invoked by db init insertion of dummy data
        elist = sess.query(Enrolled).filter_by(sid=sid).all()
        for x in elist:
            current_sched.append( (parse_time(sess.query(Course).filter_by(cid=x.cid).one()), x) )

    for x in current_sched:
        for k in x[0].keys():
            if k in q:
                if ((max(x[0][k]) >= min(q[k]) >= min(x[0][k])) | 
                    (max(x[0][k]) >= max(q[k]) >= min(x[0][k])) |
                    (min(q[k]) <= min(x[0][k]) and max(q[k]) >= max(x[0][k]))):
                     return x[1]
    return 0
    
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


def enroll_course(cid):
    d = {}
    d['cid'] = cid
    d['sid'] = current_user.id
    d['exam1'] = 0
    d['exam2'] = 0
    d['final'] = 0
    en = Enrolled(**d)
    try:
        sess.add(en)
        sess.commit()
    except cx_Oracle.DatabaseError, exc:
        error, = exc.args
        print "Code: ", error.code
        print "Message: ", error.message
        flash("Database error - Please contact your administrator")
        sess.rollback()
    

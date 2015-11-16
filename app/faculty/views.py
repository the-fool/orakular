from flask import render_template, url_for, redirect, request, flash, abort
from flask.ext.login import  login_required, current_user
from . import faculty 
from ..models import User, Student, Enrolled, Course, Faculty
from ..database import db_session as sess
from ..decorators import faculty_only

@faculty.route('/dashboard', methods=['GET', 'POST'])
@login_required
@faculty_only
def dashboard():
    try:
        f = sess.query(Faculty).filter_by(fid=current_user.id).one()
        c = []
        for course in sess.query(Course).filter_by(fid=f.fid).all():
            d = {}
            d['c'] = course
            s = []
            for e in sess.query(Enrolled).filter_by(cid=course.cid).all():
               s.append(
                   {'student':sess.query(Student).filter_by(sid=e.sid).one(), 
                    'grades':e }
               )
               d['s'] = s
            c.append(d)
    except:
        raise
    return render_template('faculty/dashboard.html', 
                           faculty=f, courses=c)

@faculty.route('/course_info/<cid>', methods=['GET', 'POST'])
@login_required
@faculty_only
def course_info(cid):
    course = sess.query(Course).filter_by(cid=cid).one()
    enrolled = sess.query(Enrolled).filter_by(cid=cid).all()
    students = [ {'s':sess.query(Student).filter_by(sid=x.sid).one(), 
                  'e1': x.exam1, 'e2':x.exam2, 'f':x.final} for x in enrolled]
    instructor = sess.query(Faculty).filter_by(fid=course.fid).one().fname
    back = request.referrer
    if not back or back.find('login') != -1: # bad hack
        back = url_for('main.index')
    
    return render_template('course_info.html', course=course, students=students,
                           instructor=instructor, enrolled=enrolled, back=back)

@faculty.route('/edit_grade', methods=['POST'])
@login_required
@faculty_only
def edit_grade():
    pass

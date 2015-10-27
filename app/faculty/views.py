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
            s = []
            for e in sess.query(Enrolled).filter_by(cid=course.cid).all():
               s.append((sess.query(Student).filter_by(sid=e.sid).one(), e))
            c.append((course, s))
    except:
        raise
    
    return render_template('faculty/dashboard.html', 
                           faculty=f, courses=c)


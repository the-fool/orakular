from flask import render_template, url_for, redirect, request, flash, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import student
from ..models import User, Student, Enrolled, Course, Faculty
from .forms import LoginForm
from ..database import db_session as sess
from ..decorators import student_only

@student.route('/dashboard', methods=['GET', 'POST'])
@login_required
@student_only
def profile():
    try:
        s = sess.query(Student).filter_by(sid=current_user.id).one()
        e = sess.query(Enrolled).filter_by(sid=s.sid).all()
        c = {}
        for x in e:
            c[x.cid]= sess.query(Course).filter_by(cid=x.cid).one()
    except:
        raise
    
    return render_template('student/dashboard.html', s=s, e=e, c=c)


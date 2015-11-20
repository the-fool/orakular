from flask import render_template, url_for, redirect, request, flash, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import student
from ..models import User, Student, Enrolled, Course, Faculty
from .forms import LoginForm
from ..database import db_session as sess
from ..decorators import student_only

@staff.route('/dashboard', methods=['GET', 'POST'])
@login_required
@staff_only
def dashboard():
    try:
        did = sess.query(Staff.deptid).filter_by(sid=current_user.id).one()
    except:
        raise
    return render_template('staff/dashboard.html', student=s, enrollment=e, courses=c)


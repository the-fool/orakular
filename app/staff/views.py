from flask import render_template, url_for, redirect, request, flash, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import staff
from ..models import User, Staff, Student, Department, Enrolled, Course, Faculty
from .forms import LoginForm
from ..database import db_session as sess
from ..decorators import staff_only

@staff.route('/dashboard', methods=['GET', 'POST'])
@login_required
@staff_only
def dashboard():
    try:
        staff = sess.query(Staff).filter_by(sid=current_user.id).one()
        department = sess.query(Department).filter_by(did=staff.deptid).one()
        c_list = (sess
                  .query(Course, Faculty)
                  .filter(Faculty.deptid == staff.deptid)
                  .join(Faculty)
                  .all() 
        )
        c_list = [ {'c': x[0], 'f': x[1]} for x in c_list]
        
        e_list = (sess
                  .query(Enrolled, Student)
                  .filter(Enrolled.cid.in_([x['c'].cid for x in c_list]))
                  .join(Student)
                  .all())
        e_list = [ {'e': x[0], 's': x[1]} for x in e_list] 
        
        for x in c_list:
            x['es'] = []
            for z in e_list:
                if z['e'].cid == x['c'].cid:
                    x['es'].append(z)
        print c_list
    except:
        raise

    return render_template('staff/dashboard.html', staff=staff, department=department, c_list = c_list)
    return "pass"

@staff.route('/edit_grade', methods=['GET','POST'])
@login_required
@staff_only
def edit_grade():
    pass

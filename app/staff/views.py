from flask import Response, render_template, url_for, redirect, request, flash, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import staff
from ..models import User, Staff, Student, Department, Enrolled, Course, Faculty
from .forms import LoginForm
from ..database import db_session as sess
from ..decorators import staff_only
import cx_Oracle

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

    except:
        raise

    return render_template('staff/dashboard2.html', staff=staff, department=department, c_list = c_list)


@staff.route('/edit_grade', methods=['GET','POST'])
@login_required
@staff_only
def edit_grade():
    cid = request.form['pk'].split('_')
    test = request.form['name']
    value = request.form['value']

    try:
        sess.execute("update enrolled set {0} = {1} where cid = '{2}' and sid = {3}"
                     .format(test, value, cid[1], cid[0]))
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print "DB Error: {0} - {1}".format(error.code, error.message)
        return Response(status=400)
    sess.commit()    
    return Response(status=200)

@staff.route('/courses')
@login_required
@staff_only
def course_info():
    pass
        

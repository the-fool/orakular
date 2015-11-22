from flask import Response, render_template, url_for, redirect, request, flash, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import staff
from ..models import User, Staff, Student, Department, Enrolled, Course, Faculty
from .forms import AddCourseForm
from ..database import db_session as sess, cursor as c, db
from ..decorators import staff_only
import cx_Oracle

@staff.route('/dashboard', methods=['GET', 'POST'])
@login_required
@staff_only
def dashboard():
    add_course_form = AddCourseForm()
    staff = sess.query(Staff).filter_by(sid=current_user.id).one()
    f_set = [(str(x[0]), x[1].title()) for x 
             in sess.query(Faculty.fid, Faculty.fname).filter_by(deptid = staff.deptid).all()]
    add_course_form.faculty.choices =  f_set
    
    if add_course_form.validate_on_submit():
        print "validating " + add_course_form.faculty.data
        try:
            add_course_form.cname.data = add_course_form.cname.data.replace("'", "''")
            print add_course_form.cname.data
            c.execute("INSERT INTO courses (cid, cname, fid, meets_at, room, limit) VALUES ('{0}', '{1}', '{2}', 'M 0:00', 'none', 99)"
                      .format(str(add_course_form.cid.data).upper(), add_course_form.cname.data
                              , str(add_course_form.faculty.data)))
            db.commit()
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print "DB Error: {0} -- {1}".format(error.code, error.message)
            db.rollback()
            if error.code == 1:
                flash('Primary key constraint: Failed to add course')
            else: flash('Failed to add course.')
    else:
        print "not validating"
    try:
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

    return render_template('staff/dashboard2.html', staff=staff, department=department, c_list = c_list, add_course_form = add_course_form)


@staff.route('/edit_grade', methods=['GET','POST'])
@login_required
@staff_only
def edit_grade():
    cid = request.form['pk'].split('_')
    test = request.form['name']
    value = request.form['value']

    try:
        c.execute("update enrolled set {0} = {1} where cid = '{2}' and sid = {3}"
                     .format(test, value, cid[1], cid[0]))
        db.commit()
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print "DB Error: {0} - {1}".format(error.code, error.message)
        db.rollback()
        return Response(status=400)
    
    return Response(status=200)

@staff.route('/courses')
@login_required
@staff_only
def course_info():
    pass

@staff.route('/update_course', methods=['GET', 'POST'])
@login_required
@staff_only
def update_course():
    pk = request.form['pk']
    attr = request.form['name']
    val = request.form['value']
  
    
    try:
        c.execute("update courses set {0} = '{1}' where cid = '{2}'".format(attr, val, pk))
        db.commit()
    except cx_Oracle.DatabaseError as ex:
        error, = ex.args
        print "DB Error: {0} - {1}".format(error.code, error.message)
        db.rollback()
        if str(error.code) == '20001':
            print '***'
            return Response('Registration limit is incompatible with enrollment', status=409)
            
        return Response(status=400)
   
    return Response(status=200)


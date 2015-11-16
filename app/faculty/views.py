from flask import render_template, url_for, redirect, request, flash, abort, make_response, Response
from flask.ext.login import  login_required, current_user
from . import faculty 
from ..models import Department, User, Student, Enrolled, Course, Faculty
from ..database import db_session as sess
from ..decorators import faculty_only
import cx_Oracle

@faculty.route('/dashboard', methods=['GET', 'POST'])
@login_required
@faculty_only
def dashboard():
    try:
        f = sess.query(Faculty).filter_by(fid=current_user.id).one()
        department = sess.query(Department).filter_by(did=f.deptid).one()
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
                           faculty=f, courses=c, department=department)

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
    cid = request.form['pk'].split('_')
    test = request.form['name']
    value = request.form['value']
    if cid[1] in [x.cid for x in 
                   sess.query(Course).filter_by(fid=current_user.id).all()]:
        try:
            sess.execute("update enrolled set {0} = {1} where sid = {2} and cid = '{3}'"
                     .format(test, value, cid[0], cid[1]))
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print "DB Error: {0} - {1}".format(error.code, error.message)
            return Response(status=400)
            
        return Response(status=200)
    else:
        return Response(status=400)

from flask import render_template, session, redirect, url_for, request, jsonify, flash, current_app, Response
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import main
from ..student import student, views as student_func
import cx_Oracle
from ..database import db_session as sess
from ..models import Student, Faculty, Course, Department, Enrolled, Staff, User
from ..auth.forms import LoginForm
from ..decorators import non_student_only
import json
from sqlalchemy import func
from itertools import chain

@main.route("/", methods=['GET', 'POST'])
def index():
    form = LoginForm()       
    if form.validate_on_submit():
        user = User.check_user(id=form.id.data)
        if user is not None:
            login_user(user, form.remember_me.data)
            flash('Welcome to the Bureaucalypse!')
        else:
            flash('Invalid User ID')
        return redirect(url_for('.index'))
    if current_user.is_authenticated:
       return redirect(url_for('{0}.dashboard'.format(current_user.role)))
    else: 
        return render_template('index.html', 
                           form=form, 
			   id_no=session.get('id_no'))

@main.route("/courses")
def courses():
    if current_user.is_authenticated:
        if current_user.role == 'student':
            return redirect(url_for('student.courses'))
    c_list = []
    f_dict = {}
    for f in sess.query(Faculty).all():
        f_dict[f.fid] = f.fname
    for c in sess.query(Course).all():    
        c_list.append({'c': c, 'f': f_dict[c.fid]})
  
    return render_template("courses.html", form=None,
                             courses=c_list) 
@main.route("/dep")
def departments():
    return redirect(url_for('.department_home', did=0))

@main.route("/dep/<int:did>")
def department_home(did):
    l = []
    try:
        for d in sess.query(Department).all():
            dic = {}
            f_list = sess.query(Faculty).filter_by(deptid=d.did).all()
            s_list = sess.query(Staff).filter_by(deptid=d.did).all()
            c_list = []
            for c in sess.query(Course).all():
                if c.fid in [f.fid for f in f_list]:  # O(n^2)
                    c_list.append(c)
            dic = {'f':f_list, 's':s_list, 'c':c_list, 'd':d}
            l.append(dic)
        return render_template('departments.html', l=l, active=did)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print "DB Error: {0} -- {1}".format(error.code, error.message)
        raise


@main.route('/course_info/<cid>', methods=['GET', 'POST'])
@login_required
@non_student_only
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


@main.route("/ajax/student_modal")
@login_required
@non_student_only
def gen_student_modal():
    sid = request.args.get('sid','')
    try:
        student = sess.query(Student).filter_by(sid=sid).one()
        enrolled = sess.query(Enrolled).filter_by(sid=sid).all()
        e_list = [ {'c':sess.query(Course).filter_by(cid=x.cid).one(), 
                    'e':x} 
                   for x in enrolled]

        return render_template('student_modal_gen.html', 
                               s=student, e_list=e_list)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print "DB Error: {0} -- {1}".format(error.code, error.message)
        raise
        
@main.route("/search")
@login_required
@non_student_only
def search():
    return render_template('search.html')


@main.route("/api/<target>")
def api(target):
    args = request.args
 
    l = []
    if target.lower() == 'enrolled':
        l = apiEnrolled(args)
    elif target.lower() == "course":
        l = apiCourse(args)
    elif target.lower() == 'student':
        l = apiStudent(args)
    elif target.lower() == 'faculty':
        l = apiFaculty(args)
    elif target.lower() == 'personnel':
        l = apiPersonnel(args)
    else:
        t = globals()[target.title()] 
        l = table_to_dict(sess.query(t).all())
    
        
    return Response(json.dumps(l), content_type='application/json', mimetype='application/json')

@main.route("/api/update/<target>", methods=['GET', 'POST', 'DELETE', 'PUT'])
def update(target):
    j = request.get_json()
    print j
    if request.method == 'POST':
        if target.lower() == "enrolled":
            conflicts = []
            cid = str(request.json['cid'])
            sid = request.json['sid']
            if not isinstance(sid, list):
                sid = [sid]
            for s in sid:
                s = int(s)
                print s
                check = student_func.check_schedule(cid, s)
                if check == 0:
                    sess.execute("INSERT INTO ENROLLED (sid, cid, exam1, exam2, final) VALUES ({0}, '{1}', 0, 0, 0)".format(s, cid))
                    sess.commit()
                    print "enrolled"
                else:
                    conflicts.append( {'sid':s,'cid':check.cid})
                    print "error on enrollment"
            print conflicts
            return Response(json.dumps(conflicts), content_type='application/json', 
                            mimetype='application/json')
    elif request.method=='DELETE':
        if target.lower()=='enrolled':
            cid = str(request.json['cid'])
            sid = request.json['sid']
 
            if not isinstance(sid, list):
                sid = [sid]
            try:
                for s in sid:
                    print "trying"
                    s = int(s)
                    sess.execute("DELETE FROM ENROLLED WHERE sid={0} AND cid='{1}'"
                                 .format(s,cid)) 
                    print "exected"
                    sess.commit()
                return 'ok', 200
            except:
                raise
                return 'not ok', 400
        elif target.lower() == 'personnel':
            try:
                for j in request.get_json():
                    if j['role'].lower() == 'staff':
                        t,a = 'staff','sid'
                    else:
                        t,a = 'faculty','fid'
                    sess.execute("DELETE FROM {0} WHERE {1}={2}".format(t,a,j['id']))
                return 'Deleted!', 200
            
            except cx_Oracle.DatabaseException as e:
                print e
                return 'Error on delet', 400
                    
        elif target.lower() == 'course':
            cid = request.json['cid']
            
            if not isinstance(cid, list):
                cid = [cid]
            try:
                for c in cid:
                    sess.execute("DELETE FROM Courses WHERE cid='{0}'".format(str(c)))
                    sess.commit()
                    print 'deleted'
                return "alright", 200
            except:
                raise
                                 
    return 'not implemented', 400

def apiPersonnel(args):
    l = []
    ll = []
    f = args.get('filter')
    if f:
        f = f.split('_')
        if f[0].lower() == 'deptid':
            l = sess.query(Faculty).filter(Faculty.deptid==f[1]).all()
            for x in l:
                ll.append({'id': x.fid, 'name': x.fname.title(), 'role': 'Faculty'})
            l = sess.query(Staff).filter(Staff.deptid==f[1]).all()
            for x in l:
                ll.append({'id': x.sid, 'name': x.sname.title(), 'role': 'Staff'})
    return ll


def reverseName(name):
    return ', '.join(name.split()[::-1]).title()


def apiFaculty(args):
    l = []
    f = args.get('filter')
    if f:
        f = f.split('_')
        if f[0].lower()=='deptid':
            f[0] = 'did'
            l = table_to_dict( sess.query(Faculty)
                               .filter(
                                   Faculty.deptid.in_([x[0] for x in
                                                       sess.query(Department.did)
                                                       .filter_by(**{f[0]:f[1]}).all()]
                                                  )
                               ).all() )

    else:
        l = table_to_dict(sess.query(Faculty).all())
    
    if args.get('xedit'):
        for x in l:
            x['value'] = x['fid']
            x['text'] = '{0}: {1}'.format(x['fid'],x['fname'])
    return l


def apiStudent(args):
    l = []
    f = args.get('filter')
    if f:
        f = f.split('_')
        if f[0].lower() == 'cid':
            if args.get('not'):
                l = table_to_dict( sess.query(Student)
                               .filter(
                                   Student.sid.notin_([x[0] for x in
                                       sess.query(Enrolled.sid)
                                       .filter_by(**{f[0]:f[1]}).all()]
                                   )
                               ).all() )
            else:
                l = table_to_dict( sess.query(Student)
                               .filter(
                                   Student.sid.in_([x[0] for x in
                                       sess.query(Enrolled.sid)
                                       .filter_by(**{f[0]:f[1]}).all()]
                                   )
                               ).all() )
                
                
    else:
        l = table_to_dict(sess.query(Student).all())
    return l
def apiCourse(args):
    l = []
    f = args.get('filter')
    j = args.get('join')
    if j:
        t2 = globals()[j.title()]
        if f:
            f = f.split('_')
            if f[0].lower() == 'deptid':
                l = table_to_dict( sess.query(Course, t2)
                                   .filter(
                                       Course.fid.in_(
                                           [x[0] for x in
                                            sess.query(Faculty.fid)
                                            .filter_by(**{f[0]:f[1]}).all()
                                        ]
                                       )
                                   )
                                   .join(t2).all() )
      
            else:
                l = table_to_dict( sess.query(Course, t2)
                                   .filter_by(**{f[0]:f[1]})
                                   .join(t2)
                                   .all()
                               )
        else:
            l = table_to_dict(sess
                              .query(Course, t2)
                              .join(t2)
                              .all() )
    elif f:
        f = f.split('_')
        if f[0].lower() == 'deptid':
            l = table_to_dict( sess.query(Course)
                               .filter(
                                   Course.fid.in_(
                                       [x[0] for x in
                                        sess.query(Faculty.fid)
                                        .filter_by(**{f[0]:f[1]}).all()
                                    ]
                                   )
                               ).all() )
        else:
            l = table_to_dict(sess.query(Course)
                          .filter_by(**{f[0]: f[1]})
                          .all())
    else:
        l = table_to_dict(sess.query(Course).all())
    
    if args.get('c_avg'):
        d = {}
        e = sess.query(Enrolled).all()
        for x in e:
            if x.cid in d:
                d[x.cid] += (x.exam1 + x.exam2 + x.final)/3
                d[x.cid + "_len"] += 1
            else:
                d[x.cid] = (x.exam1 + x.exam2 + x.final)/3
                d[x.cid + "_len"] = 1
        for x in l:
            if x['cid'] in d:
                x['c_avg'] = str(d[x['cid']] / d[x['cid']+"_len"])

    e = dict(sess.query(Enrolled.cid, 
                        func.count(Enrolled.sid))
             .group_by(Enrolled.cid).all())
    
    for x in l:
        if x['cid'] in e:
            x['active'] = e[x['cid']]
        else:
            x['active'] = 0
    
    return l

def apiEnrolled(args):
    l = []
    f = args.get('filter')
    j = args.get('join')
    if f:
        f = f.split('_')
        if j:
            t2 = globals()[args.get('join').title()]
            l = table_to_dict(sess.query(Enrolled, t2)
                              .filter_by(**{f[0]: f[1]})
                              .join(t2).all())
        else:
            l = table_to_dict(sess.query(Enrolled).filter_by(**{f[0]: f[1]}).all())
    elif args.get('join'):
        try:
            t2 = globals()[args.get('join').title()]
        except:
            pass
        l = table_to_dict(sess.query(Enrolled, t2).join(t2).all())
    else:
        l = table_to_dict(sess.query(Enrolled).all())
    if args.get('s_avg'):
        for x in l:
            x['avg'] = str( (float(x['exam1']) + float(x['exam2']) 
                             + float(x['final']) ) /3)
    return l

def table_to_dict(table):
    l = []
    for row in table:
        d = {}
        if not isinstance(row, tuple):
            row = row,
        row = list(row)
        for r in row:
            for column in r.__table__.columns:
                d[column.name] = str(getattr(r, column.name))
                if column.name in ['sname', 'fname']:
                    d[column.name] = ', '.join(d[column.name].split()[::-1])
                if column.name not in ["cid", "meets_at"]:
                    d[column.name] = d[column.name].title()
        l.append(d)
    return l


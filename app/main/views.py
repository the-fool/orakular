from flask import render_template, session, redirect, url_for, request, jsonify, flash, current_app, Response
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import main
from ..student import student
import cx_Oracle
from ..database import db_session as sess
from ..models import Student, Faculty, Course, Department, Enrolled, Staff, User
from ..auth.forms import LoginForm
from ..decorators import non_student_only
import cx_Oracle
import json
from sqlalchemy import func


@main.route("/", methods=['GET', 'POST'])
def index():
    form = LoginForm()       
    if form.validate_on_submit():
       user = User.check_user(id=form.id.data)
       if user is not None:
           login_user(user, form.remember_me.data)
           flash('hello member')
       else:
           flash('invalid id')
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

    course_list = sess.query(Course).all()    
    return render_template("courses.html", form=None,
                           courses=course_list) 


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
    
@main.route("/search")
@login_required
@non_student_only
def search():
    return render_template('search.html')


@main.route("/api/<target>")
def api(target):
    args = request.args
    t = globals()[target.title()]
    l = []
    if target.lower() == 'enrolled':
        l = apiEnrolled(args)
    elif target.lower() == "course":
        l = apiCourse(args)
       
    else:
        l = table_to_dict(sess.query(t).all())
    
    return Response(json.dumps(l), mimetype='application/json')

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
            x['c_avg'] = str(d[x['cid']] / d[x['cid']+"_len"])

    e = dict(sess.query(Enrolled.cid, 
                        func.count(Enrolled.sid))
             .group_by(Enrolled.cid).all())
    for x in l:
        x['active'] = e[x['cid']]
    
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


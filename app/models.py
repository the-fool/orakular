# coding: utf-8
from sqlalchemy import Numeric, Column, ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import relationship
from database import Base, db_session
from . import login_manager

metadata = Base.metadata


class Course(Base):
    __tablename__ = 'courses'

    cid = Column(String(16), primary_key=True)
    cname = Column(String(50), nullable=False)
    meets_at = Column(String(30))
    room = Column(String(15))
    fid = Column(ForeignKey(u'faculty.fid'))
    limit = Column(Numeric(scale=0, asdecimal=False))
    faculty = relationship(u'Faculty')


class Department(Base):
    __tablename__ = 'department'

    did = Column(Integer, primary_key=True)
    dname = Column(String(50))


class Enrolled(Base):
    __tablename__ = 'enrolled'

    sid = Column(ForeignKey(u'students.sid'), primary_key=True, nullable=False)
    cid = Column(ForeignKey(u'courses.cid'), primary_key=True, nullable=False)
    exam1 = Column(Numeric(scale=0, asdecimal=False))
    exam2 = Column(Numeric(scale=0, asdecimal=False))
    final = Column(Numeric(scale=0, asdecimal=False))

    course = relationship(u'Course')
    student = relationship(u'Student')


class Faculty(Base):
    __tablename__ = 'faculty'

    fid = Column(Integer, primary_key=True)
    fname = Column(String(50))
    deptid = Column(ForeignKey(u'department.did'))

    department = relationship(u'Department')


class Staff(Base):
    __tablename__ = 'staff'

    sid = Column(Integer, primary_key=True)
    sname = Column(String(50))
    deptid = Column(ForeignKey(u'department.did'))

    department = relationship(u'Department')


class Student(Base):
    __tablename__ = 'students'

    sid = Column(Integer, primary_key=True)
    sname = Column(String(50), nullable=False)
    major = Column(String(30), nullable=False, server_default=text("'undeclared' "))
    s_level = Column(String(15), nullable=False)
    age = Column(Integer)


t_test = Table(
    'test', metadata,
    Column('i', Numeric(scale=0, asdecimal=False)),
    Column('name', String(15))
)

class User():
    USERS = {}
    
    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def is_anonymous(self):
        return False
        
    @classmethod
    def check_user(cls, id, role):
        id = int(id)
        role = role.encode('ascii')
        u = User.USERS.get(id)
        if u is not None:
            return u
        if role == 'student':
            try:
                s = db_session.query(Student).filter_by(sid=id).one()
            except:
                s = None
            if s is not None:
                u = User(id=s.sid, name=s.sname, role='student')
                User.USERS[id] = u
                return u
        elif role == 'faculty':
            try:
                f = db_session.query(Faculty).filter_by(fid=id).one()
            except:
                f = None
            if f is not None:
                u = User(id=f.fid, name=f.fname, role='faculty')
                User.USERS[id] = u
                return u
        elif role == 'staff':
            try:
                s = db_session.query(Staff).filter_by(sid=id).one()
            except:
                s = None
            if s is not None:
                u = User(id=s.sid, name=s.sname, role='staff')
                User.USERS[id] = u
                return u
        return None
                
@login_manager.user_loader
def load_user(user_id):
    return User.USERS.get(int(user_id))

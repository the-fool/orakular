# coding: utf-8
from sqlalchemy import Column, ForeignKey, Numeric, String, Table, text
from sqlalchemy.orm import relationship
from database import Base

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

    did = Column(Numeric(scale=0, asdecimal=False), primary_key=True)
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

    fid = Column(Numeric(scale=0, asdecimal=False), primary_key=True)
    fname = Column(String(50))
    deptid = Column(ForeignKey(u'department.did'))

    department = relationship(u'Department')


class Staff(Base):
    __tablename__ = 'staff'

    sid = Column(Numeric(scale=0, asdecimal=False), primary_key=True)
    sname = Column(String(50))
    deptid = Column(ForeignKey(u'department.did'))

    department = relationship(u'Department')


class Student(Base):
    __tablename__ = 'students'

    sid = Column(Numeric(scale=0, asdecimal=False), primary_key=True)
    sname = Column(String(50), nullable=False)
    major = Column(String(30), nullable=False, server_default=text("'undeclared' "))
    s_level = Column(String(15), nullable=False)
    age = Column(Numeric(scale=0, asdecimal=False))


t_test = Table(
    'test', metadata,
    Column('i', Numeric(scale=0, asdecimal=False)),
    Column('name', String(15))
)

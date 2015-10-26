from app.models import Course, Department, Enrolled, Faculty, Staff, Student
from app.database import db_session as sess, cursor, db
from random import randint, shuffle
from database import db

db.ex("database/db_config.sql")
db.ex("database/data.sql")

# set course fid to the correct faculty fid
lf = sess.query(Faculty).all()
lc = sess.query(Course).all()
for f, c in zip(lf, lc):
    c.fid = f.fid
sess.commit()
    

ls = sess.query(Student).all()
for s in ls:
    tmp = lc[:]
    shuffle(tmp)
    i = 0
    while i < 3:
        d = {}
        d["cid"] = tmp.pop().cid
        d["sid"] = s.sid
        d["exam1"] = randint(50,100)
        d["exam2"] = randint(55,100)
        d["final"] = randint(55,100)
        en = Enrolled(**d)
        try: 
            sess.add(en)
            sess.commit()
        except:
            sess.rollback()
            i -= 1
        i += 1
            
        

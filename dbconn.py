import cx_Oracle
from config import DBNAME, DBPASSWORD, DBADDRESS

curs = None
db = None
def conn():
  global db
  db = cx_Oracle.connect(DBNAME, DBPASSWORD, DBADDRESS)
  global curs 
  curs = db.cursor()
def ex(command):
  if curs is None:
    conn()
  ret = curs.execute(command)
  db.commit()
  return ret
def fetch(command):
  if curs is None:
    conn()
  return curs.execute(command).fetchall()

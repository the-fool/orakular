import os, sys
DIR = '/var/www/cs430_project'
sys.path.append(DIR)
import cx_Oracle
from config import DBNAME, DBPASSWORD, DBADDRESS

def ex(source):
 with open(source) as script:
  db = cx_Oracle.connect(DBNAME, DBPASSWORD, DBADDRESS)
  c = db.cursor()
  txt = ''
  while True:
    buf = script.read(1024) 
    if not buf: break
    txt += buf
  
  commands = txt.split('/')    
  for command in commands:
    try:
      print "\n\nExecuting:\n" + command
      c.execute(command)
      db.commit()
    except cx_Oracle.DatabaseError, ex:
      error, = ex.args
      print '*****ERROR*****\n'
      print 'Error.code =', error.code
      print 'Error.message =', error.message
      print 'Error.offset =', error.offset
      db.rollback()


if __name__ == '__main__':
  ex(sys.argv[1])

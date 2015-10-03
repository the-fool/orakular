import os, sys
DIR = '/var/www/cs430_project'
sys.path.append(DIR)
import cx_Oracle
from config import DBNAME, DBPASSWORD, DBADDRESS

db = cx_Oracle.connect(DBNAME, DBPASSWORD, DBADDRESS)
c = db.cursor()

txt = ''
with open('db_script.sql') as script:
  while True:
    buf = script.read(1024) 
    if not buf: break
    txt += buf
  
  commands = txt.split('/')    
  for command in commands:
    try:
      print "Executing: " + command
      c.execute(command)
      db.commit()
    except cx_Oracle.DatabaseError, ex:
      error, = ex.args
      print 'Error.code =', error.code
      print 'Error.message =', error.message
      print 'Error.offset =', error.offset
      db.rollback()


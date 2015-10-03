import os, sys
DIR = '/var/www/cs430_project'
sys.path.append(DIR)
import cx_Oracle
from config import DBNAME, DBPASSWORD, DBADDRESS

db = cx_Oracle.connect(DBNAME, DBPASSWORD, DBADDRESS)

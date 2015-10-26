from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DBNAME, DBPASSWORD, DBADDRESS
import cx_Oracle

engine = create_engine('oracle://{0}:{1}@{2}'.format(DBNAME, DBPASSWORD, DBADDRESS, convert_unicode=True))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

db = cx_Oracle.connect(DBNAME, DBPASSWORD, DBADDRESS)
cursor = db.cursor()


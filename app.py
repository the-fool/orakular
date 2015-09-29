from flask import Flask, render_template
import cx_Oracle
from flask.ext.bootstrap import Bootstrap
from config import DBNAME, DBPASSWORD, DBADDRESS

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route("/data/")
def hello():
	db = cx_Oracle.connect(DBNAME, DBPASSWORD, DBADDRESS)
	c = db.cursor()
	c.execute("select * from test")
	r = c.fetchall()
	s = ""
	for tup in r:
	  s += str(tup)
	return "here is your data: " + s

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

if __name__ == '__main__':
	app.run()

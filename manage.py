#!/var/www/cs430project/venv/bin python
import os
from app import create_app
from flask.ext.script import Manager, Shell
from app.models import Course, User, Student, Faculty, Staff

app = create_app(os.path.abspath("config.py"))
manager = Manager(app)

def make_shell_context():
    return dict(app=app, Student=Student, Faculty=Faculty, Staff=Staff, Course=Course)
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

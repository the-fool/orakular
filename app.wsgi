import os, sys

DIR = '/var/www/cs430_project'

activate_this = '/var/www/cs430_project/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
sys.path.append(DIR)

from app import app as application

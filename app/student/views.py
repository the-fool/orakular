from flask import render_template, url_for, redirect, request, flash
from flask.ext.login import login_user, logout_user, login_required
from . import student
from ..models import User
from .forms import LoginForm
from ..database import db_session
from ..decorators import student_only

@student.route('/dashboard', methods=['GET', 'POST'])
@login_required
@student_only
def profile():
    return render_template('student/dashboard.html')


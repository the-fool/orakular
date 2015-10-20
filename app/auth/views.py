from flask import render_template, url_for, redirect, request, flash
from flask.ext.login import login_user
from . import auth
from ..models import User
from .forms import LoginForm
from ..database import db_session

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #user = User(id=form.id.data, role=form.role.data, name=form.name.data)
        #login_user(user, form.remember_me.data)
        #return redirect(url_for('main.index'))
	return "Hello!"
    return render_template('auth/login.html', form=form)

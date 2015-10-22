from flask import render_template, url_for, redirect, request, flash
from flask.ext.login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm
from ..database import db_session

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.check_user(id=form.id.data
                               , role=form.role.data)
        if user is not None:
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') 
                            or url_for('main.index'))
        flash('Invalid ID')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

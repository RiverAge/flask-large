from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user

from ..models import User
from ..email import send_mail
from .forms import LoginForm, RegistrationForm
from app import db

from . import auth

@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm();
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('you have success logged in!', 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'warning')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(user.email, 'confirm you account', 'auth/email/confirm', user=user, token=token)
        flash('a confirmation email has benn sent to you by email', 'info')
        flash('You can now login.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

from flask import Blueprint, render_template
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.model import User, Role
from app.auth.forms import LoginForm, RegistrationForm
from app import db


@bp.route('/login',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    session['mssg'] = ""
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            session['mssg'] = "Invalid Username or Password"
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('main.home'))

    return render_template('auth/login.html', title=('Log In'), form=form, mssg=session['mssg'])


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    session['mssg'] = ""
    if form.validate_on_submit():
        if str(form.key.data) == "admin":
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            role = Role.query.filter_by(name="ADMIN").first()
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()
            session['mssg'] = "Thanks for Signing Up . Please login to use Hafta"
            return redirect(url_for('auth.login'))
        else:
            session['mssg'] = "Invalid Key"
    return render_template('auth/register.html', title='Register',
                           form=form, mssg=session['mssg'])


@bp.route('/remove/session', methods=['POST'])
def remove_mssg():
    session['mssg'] = ""
    return jsonify({'mssg': 'Emptying session mssg'})

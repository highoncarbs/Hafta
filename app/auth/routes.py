from flask import Blueprint, render_template
from flask import render_template, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.model import User , Role
from app.auth.forms import LoginForm, RegistrationForm
from app import db

@bp.route('/login' ,  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            session['mssg'] = "Invalid Username or Password"
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('main.home'))
    else:
        print(form.errors)
        session['mssg'] = "Something went wrong."

    return render_template('auth/login.html', title=('Log In'), form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit() and str(form.key.data) == "jaitexart":
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        role = Role.query.filter_by(name="ADMIN").first()
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        session['mssg'] = "Thanks fro Signing Up . Please login to use Hafta"
        return redirect(url_for('auth.login'))
    else:
        print(form.errors)
        session['mssg'] = "Invalid Key"
    return render_template('auth/register.html', title='Register',
                           form=form)

from flask import Blueprint, render_template
from flask import render_template, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user , login_required
from app.main import bp
from app.model import User , Role
from app import db



@bp.route('/' , methods=['GET' , 'POST'])
@bp.route('/home' , methods=['GET' , 'POST'])
@login_required
def home():
    return render_template('base/base.html', title=('Home'))

@bp.route('/employees' , methods=['GET'])
@login_required
def employees():
    return render_template('employees/index.html')

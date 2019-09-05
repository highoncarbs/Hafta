from flask import Blueprint, render_template
from flask import render_template, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user , login_required
from app.employee import bp
from app.model import User , Role
from app import db

@bp.route('/new' , methods=['GET'])
@login_required
def new():
    return render_template('employees/entry.html')

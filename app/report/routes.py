from flask import Blueprint, render_template
from flask import render_template, redirect, url_for, request, session , jsonify
from flask_login import login_user, logout_user, current_user , login_required
from app.report import bp
from app.model import User , Role
from app import db



@bp.route('/salary_slips' , methods=['GET' , 'POST'])
@login_required
def view_slips():
    return render_template('reports/salary_slips.html', title=('Report - Salary Sheet'))

@bp.route('/salary_sheet' , methods=['GET' , 'POST'])
@login_required
def view_sheet():
    return render_template('reports/salary_sheet.html', title=('Report - Salary Sheet'))

@bp.route('/advance' , methods=['GET' , 'POST'])
@login_required
def view_advance():
    return render_template('reports/advance.html', title=('Report - Salary Sheet'))

@bp.route('/attendence' , methods=['GET' , 'POST'])
@login_required
def view_attendence():
    return render_template('reports/attendence.html', title=('Report - Salary Sheet'))

@bp.route('/performance' , methods=['GET' , 'POST'])
@login_required
def view_performance():
    return render_template('reports/performance.html', title=('Report - Salary Sheet'))


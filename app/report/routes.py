from app import db
from app.model import User, Role
from app.report import bp
from flask import Blueprint, render_template
from flask import render_template, redirect, url_for, request, session, jsonify


@bp.route('/salary_slips', methods=['GET', 'POST'])
def view_slips():
    return render_template('reports/salary_slips.html', title=('Report - Salary Sheet'))


@bp.route('/salary_sheet', methods=['GET', 'POST'])
def view_sheet():
    return render_template('reports/salary_sheet.html', title=('Report - Salary Sheet'))


@bp.route('/advance', methods=['GET', 'POST'])
def view_advance():
    return render_template('reports/advance.html', title=('Report - Salary Sheet'))


@bp.route('/attendence', methods=['GET', 'POST'])
def view_attendence():
    return render_template('reports/attendence.html', title=('Report - Salary Sheet'))


@bp.route('/performance', methods=['GET', 'POST'])
def view_performance():
    return render_template('reports/performance.html', title=('Report - Salary Sheet'))

from flask import Blueprint, render_template
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_required
from app.main import bp
from app.master.model import Company, CompanySchema
from app.employee.model import Employee
from app import db


@bp.route('/firms', methods=['GET', 'POST'])
@login_required
def show_firms():
    return render_template('reports/firms.html', title=('Home'))


@bp.route('/firms/info', methods=['GET', 'POST'])
@login_required
def firms_info():
    data_schema = CompanySchema(many=True)
    data = db.session.query(Company).first().emp_company
    json_dump = data_schema.dumps(data)
    print(json_dump)
    return jsonify({'message': json_dump})

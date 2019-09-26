from flask import Blueprint, render_template
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_required
from app.main import bp
from app.master.model import Company, CompanySchema
from app.employee.model import Employee
from app import db
import json

@bp.route('/firms', methods=['GET', 'POST'])
@login_required
def show_firms():
    return render_template('reports/firms.html', title=('Firms'))


@bp.route('/firms/info', methods=['GET', 'POST'])
@login_required
def firms_info():
    data_schema = CompanySchema(many=True)
    data = db.session.query(Company).join(Employee.company).all()
    json_dump = data_schema.dumps(data)
    temp_json = json.loads(json_dump)
    for item in temp_json:
        all_emp = db.session.query(Company).filter_by(id=int(item['id'])).first().emp_company
        item['total_emp'] = len(all_emp)
        item['total_pay'] = 0
        for emp in all_emp:
            item['total_pay'] += float(emp.basicpay)

    json_dump = json.dumps(temp_json)
    return jsonify(json_dump)

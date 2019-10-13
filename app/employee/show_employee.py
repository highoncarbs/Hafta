from flask import Blueprint, render_template
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_required
from app.employee import bp
from app.employee.model import Employee, EmployeeSchema, EmployeeBasicSchema , EmployeeMainSchema
from app.master.model import Company ,CompanySchema
from app import db

# Removed Deleted employee from attendence

@bp.route('/', methods=['GET'])
@login_required
def show_employee():
    return render_template('employees/index.html')


@bp.route('/get/detail/<id>', methods=['POST'])
def get_detail(id):
    if request.method == 'POST':
        # Gets all ifo of employee
        data_schema = EmployeeSchema()
        data = Employee.query.filter_by(id=int(id)).first()
        json_data = data_schema.dumps(data)
        return jsonify(json_data)


@bp.route('/get/basic', methods=['GET'])
def get_basic():
    if request.method == 'GET':
        data_schema = EmployeeBasicSchema(many=True)
        data = Employee.query.filter(Employee.flag != int(1)).all()
        json_data = data_schema.dumps(data)
        return jsonify(json_data)

@bp.route('/delete/<emp_id>', methods=['POST'])
def delete_employee(emp_id):


    # Need Employee delete checks
    # Adavaces
    if request.method == 'POST':
        emp = Employee.query.filter_by(id= int(emp_id)).first()
        if(emp) is not None:
            emp.flag = 1
            db.session.commit()
            return jsonify({'success' : 'Employee deleted'})
        else:
            return jsonify({'message' : 'Employee not found'})
    else:
        return jsonify({'message' : 'Invalid HTTP method'})

@bp.route('/view/detail/<emp_id>', methods=['GET' , 'POST'])
def view_employee_detail(emp_id):


    # Need Employee delete checks
    # Adavaces
    return render_template('employees/employee.html')


@bp.route('/get/by/company/<companyid>', methods=['GET'])
def get_by_company(companyid):
    if request.method == 'GET':
        # compna = Company.query.filter_by(id= int(companyid)).first().name
        employee_schema = EmployeeMainSchema(many=True)
        data = Employee.query.filter(Employee.company.any(Company.id == int(companyid)) , Employee.flag == 0  ).all()
        json_data = employee_schema.dumps(data)
        return jsonify(json_data)
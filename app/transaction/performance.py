from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user
from app.transaction import bp
from app.employee.model import Employee, EmployeeAdvanceSchema
from app.master.model import Company , Performance , PerformanceSchema

from app import db, ma
from datetime import datetime

import json


@bp.route('/performance', methods=['GET'])
def show_performance():
    return render_template('transaction/performance.html')

@bp.route('/get/performance', methods=['GET'])
def get_performance_factors():
    data_schema = PerformanceSchema(many=True)
    data = Performance.query.all()
    json_data = data_schema.dumps(data)
    print(json_data)
    return jsonify(json_data)


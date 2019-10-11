# Quick Input for Employees that will be shown at the time of
# performance Inputs

from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_required
from app.transaction import bp
from app.employee.model import Employee
from app.transaction.model_qck import QuickInput, QuickInputSchema
from app import db, ma
from datetime import datetime

import json


@bp.route('/quick', methods=['GET'])
@login_required
def show_quick():
    return render_template('transaction/quickinput.html')


@bp.route('/quick/get', methods=['POST'])
@login_required
def get_quick_emp():
    payload = request.json
    if payload is not None:
        data_schema = QuickInputSchema(many=True)
        fromdate = str(payload['fromdate']).split('-')
        fromdate = datetime(
            int(fromdate[0]), int(fromdate[1]), int(fromdate[2]))
        todate = str(payload['todate']).split('-')
        todate = datetime(
            int(todate[0]), int(todate[1]), int(todate[2]))
        data = QuickInput.query.filter(
            QuickInput.employee.any(Employee.id == int(payload['emp_id'])),
            QuickInput.date >= fromdate, QuickInput.date <= todate).all()
        json_data = data_schema.dumps(data)
        return jsonify(json_data)

    else:
        return jsonify({'message': 'Empty data recieved'})


@bp.route('/quick/add', methods=['POST'])
@login_required
def add_quick():
    payload = request.json
    if payload is not None:
        emp = Employee.query.filter_by(id=int(payload['emp_id'])).first()
        report = str(payload['report'])
        feedback = str(payload['feedback'])
        payload_date = str(payload['date']).split('-')
        payload_date = datetime(
            int(payload_date[0]), int(payload_date[1]), int(payload_date[2]))

        try:
            data = QuickInput(payload_date, report, feedback)
            data.employee.append(emp)

            db.session.add(data)
            db.session.commit()
            return jsonify({'success': 'Report added'})
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return jsonify({'message': 'Something went worng. Check logs. '})

    return jsonify({'message': 'Empty data recieved'})

from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user
from app.transaction import bp
from app.transaction.model_adv import Advance, AdvanceSchema
from app.employee.model import Employee, EmployeeAdvanceSchema
from app.master.model import Company

from app import db, ma
from datetime import datetime

import json
@bp.route('/advance/', methods=['GET'])
def show_advance():
    return render_template('transaction/advance.html')


@bp.route('/advance/employee/<id>', methods=['POST'])
def get_advance_for_emp(id):
    # Get's advance details on employees

    data_schema = EmployeeAdvanceSchema()
    data = Employee.query.filter_by(id=int(id)).first()
    json_data = data_schema.dumps(data)
    return jsonify(json_data)

@bp.route('/advance/all/<id>', methods=['GET'])
def get_advance_firm(id):
    # Get's advance details on employees
    data = Company.query.first()
    data_t = Company.query.all()[1]
    adv = Advance.query.filter(Advance.company.any(Company.id == int(id))).all()
    print(adv)
    data_schema = AdvanceSchema(many=True)
    json_data = data_schema.dumps(adv)
    print(data ,data_t , adv )
    return jsonify(json_data)
    # data_schema = EmployeeAdvanceSchema()
    # data = Employee.query.filter_by(id=int(id)).first()
    # json_data = data_schema.dumps(data)
    return jsonify({})


@bp.route('/advance/get/<emp_id>', methods=['POST'])
def get_advance(emp_id):
    # GEt Advacne history of employee
    if request.method == "POST":

        today = datetime.today()
        year_start = datetime(today.year, 1, 1)
        year_end = datetime(today.year+1, 1, 1)

        # payload_date = payload['date'].split('-')
        # payload_date = datetime(
        #     int(payload_date[0]), int(payload_date[1]), int(1))

        data = Advance.query.filter(
            Advance.employee.any(Employee.id == int(emp_id)), Advance.date >= year_start, Advance.date <= year_end).all()
        data_schema = AdvanceSchema(many=True)
        json_data = data_schema.dumps(data)
        return jsonify(json_data)
    else:
        return jsonify({'message': 'Invalid HTTP Request , use POST.'})


@bp.route('/advance/save', methods=['POST'])
def save_advance():
    if request.method == 'POST':
        payload = request.json
        if payload != None:
            payload_data = payload['data']
            payload_date = payload_data['date'].split('-')
            payload_date = datetime(
                int(payload_date[0]), int(payload_date[1]), int(payload_date[2]))

            # Date checks to be done
            table_columns = (
                'letter',
                'advanceamt',
                'cheque_no',
                'deduction_period',
                'deduction'
            )

            try:

                # Need Update cehck inside
                new_data = Advance()
                emp = Employee.query.filter_by(
                    id=int(payload['emp_id'])).first()
                comp = Company.query.filter_by(
                    id=int(payload['company_id'])).first()

                new_data.employee.append(emp)
                new_data.company.append(comp)
                for field in table_columns:
                    val = payload_data[field]
                    if val == '' or val is None:
                        continue

                    setattr(new_data, field, val)
                setattr(new_data, 'date', payload_date)
                setattr(new_data, 'trans', 'credit')

                db.session.add(new_data)
                db.session.commit()
                return jsonify({'success': 'Data Added'})

            except Exception as e:
                db.session.rollback()
                return jsonify({'message': 'Something went wrong - '+str(e)})

            return jsonify({'message': 'Something went wrong'})
        else:
            return jsonify({'message': 'Empty data.'})


@bp.route('/advance/update', methods=['POST'])
def update_advance():
    if request.method == 'POST':
        payload = request.json
        if payload != None:
            table_columns = (
                'daysatt',
                'latecomin',
                'earlygoing',
            )
            try:

                # Need Update check inside
                for item in payload:
                    saved_att = db.session.query(Attendence).filter_by(
                        id=int(item['id'])).first()
                    for field in table_columns:
                        val = item[field]
                        if val == '' or val is None:
                            continue
                        setattr(saved_att, field, val)

                    if 'tdsval' in item.keys():
                        val = item['tdsval']
                        if val == '' or val is None:
                            continue
                        setattr(saved_att, 'tds', item['tdsval'])

                    if 'esival' in item.keys():
                        val = item['esival']
                        if val == '' or val is None:
                            continue
                        setattr(saved_att, 'esi', item['esival'])

                    if 'pfval' in item.keys():
                        val = item['pfval']
                        if val == '' or val is None:
                            continue
                        setattr(saved_att, 'pf', item['pfval'])

                # db.session.add(new_data)
                db.session.commit()
                return jsonify({'success': 'Data Added'})

            except Exception as e:
                db.session.rollback()
                return jsonify({'message': 'Something went wrong'})

            return jsonify({'message': 'Something went wrong'})
        else:
            return jsonify({'message': 'Empty data.'})


@bp.route('/advance/delete/<adv_id>', methods=['POST'])
def delete_advance(adv_id):
    advance = Advance.query.filter_by(id=int(adv_id))
    if advance.first() is None:
        return jsonify({'message': 'Could not find advance transaction'})
    else:
        try:
            advance.employee = []
            advance.delete()
            db.session.commit()
            return jsonify({'success': 'Advance transaction deleted'})
        except Exception as e:
            return jsonify({'message': 'Somethign went wrong'})

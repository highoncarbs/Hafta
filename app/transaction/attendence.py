from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user
from app.transaction import bp
from app.transaction.model_att import Attendence, AttendenceSchema
from app.employee.model import Employee
from app.master.model import Company

from app import db, ma
from datetime import datetime

import json
@bp.route('/attendence/', methods=['GET'])
def show_attendence():
    return render_template('transaction/attendence.html')


@bp.route('/attendence/get', methods=['POST'])
def get_attendence():
    if request.method == "POST":
        payload = request.json
        if payload != None:
            print(payload)
            payload_date = payload['date'].split('-')
            payload_date = datetime(
                int(payload_date[0]), int(payload_date[1]), int(1))
            company = payload['company']
            data = Attendence.query.filter(
                Attendence.company.any(Company.id == int(company)), Attendence.date == payload_date).all()
            data_schema = AttendenceSchema(many=True)
            json_data = data_schema.dumps(data)
            print(json_data)
            return jsonify(json_data)
        else:
            return jsonify({'message': 'Empty Data Recieved'})

    else:
        return jsonify({'message': 'Invalid HTTP Request , use POST.'})


@bp.route('/attendence/employee/<emp_id>', methods=['GET'])
def emp_attendence(emp_id):
    if request.method == "GET":
        year = datetime(datetime.now().year,  1, 1)
        data = Attendence.query.filter(
            Attendence.employee.any(Employee.id == int(emp_id)), Attendence.date >= year).all()
        today = datetime.now()
        # new_data = db.session.extract('date', data) == today.year
        print(data[0].date)
        day_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        early_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        late_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for item in data:
            index = int(datetime.strptime(
                str(item.date).split(" ")[0], "%Y-%m-%d").month)-1
            day_att[index] = item.daysatt
            early_att[index] = item.earlygoing
            late_att[index] = item.latecomin
        json_data = json.dumps(
            {'day_att': day_att, 'early_att': early_att, 'late_att': late_att})
        print(json_data)
        return jsonify(json_data)
    else:
        return jsonify({'message': 'Invalid HTTP request method.'})


@bp.route('/attendence/employee/data/<emp_id>', methods=['POST'])
def emp_attendence_data(emp_id):
    if request.method == "POST":
        data = Attendence.query.filter(
            Attendence.employee.any(Employee.id == int(emp_id))).all()
        # data_schema = AttendenceSchema(many=True)
        today = datetime.now()
        today.year()
        return jsonify(json_data)
    else:
        return jsonify({'message': 'Invalid HTTP request method.'})


@bp.route('/attendence/save', methods=['POST'])
def save_attendence():
    if request.method == 'POST':
        payload = request.json
        if payload != None:
            payload_data = payload['data']
            payload_date = payload['date'].split('-')
            payload_date = datetime(
                int(payload_date[0]), int(payload_date[1]), int(1))
            # Date checks to be done
            table_columns = (
                'daysatt',
                'latecomin',
                'earlygoing',
                'other_deduction'

            )
            try:

                # Need Update cehck inside
                for item in payload_data:
                    print(item)
                    new_data = Attendence()
                    emp = Employee.query.filter_by(
                        id=int(item['id'])).first()
                    company = Company.query.filter_by(
                        id=int(payload['company'])).first()
                    new_data.company.append(company)
                    new_data.employee.append(emp)
                    for field in table_columns:
                        val = item[field]
                        print(val, field)
                        if val == '' or val is None:
                            continue
                        setattr(new_data, field, val)
                    setattr(new_data, 'date', payload_date)

                    if 'tdsval' in item.keys():
                        setattr(new_data, 'tds', item['tdsval'])
                    if 'esival' in item.keys():
                        setattr(new_data, 'esi', item['esival'])
                    if 'pfval' in item.keys():
                        setattr(new_data, 'pf', item['pfval'])

                db.session.add(new_data)
                db.session.commit()
                return jsonify({'success': 'Data Added'})

            except Exception as e:
                print(str(e))
                db.session.rollback()
                return jsonify({'message': 'Something went wrong'})

            return jsonify({'message': 'Something went wrong'})
        else:
            return jsonify({'message': 'Empty data.'})


@bp.route('/attendence/update', methods=['POST'])
def update_attendence():
    if request.method == 'POST':
        payload = request.json
        if payload != None:
            print('this is it --')
            print(payload)
            print('---------------')
            # payload_data = json.loads(payload['data'])
            # payload_date = str(payload['date']).split('-')
            # payload_date = datetime(
            #     int(payload_date[0]), int(payload_date[1]), int(1))
            # Date checks to be done
            # print(payload_date)
            table_columns = (
                'daysatt',
                'latecomin',
                'earlygoing',
                'other_deduction'
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
                print(str(e))
                db.session.rollback()
                return jsonify({'message': 'Something went wrong'})

            return jsonify({'message': 'Something went wrong'})
        else:
            return jsonify({'message': 'Empty data.'})

from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user
from app.transaction import bp
from app.transaction.model_att import Attendence, AttendenceSchema , CompanySchema
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
            payload_date = payload['date'].split('-')
            payload_date = datetime(
                int(payload_date[0]), int(payload_date[1]), int(1))
            company = payload['company']
            data = Attendence.query.filter(
                Attendence.company.any(Company.id == int(company)), Attendence.date == payload_date).all()
            data_schema = AttendenceSchema(many=True)
            json_data = data_schema.dumps(data)
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
        return jsonify(json_data)
    else:
        return jsonify({'message': 'Invalid HTTP request method.'})


# @bp.route('/attendence/employee/data/<emp_id>', methods=['POST'])
# def emp_attendence_data(emp_id):
#     if request.method == "POST":
#         data = Attendence.query.filter(
#             Attendence.employee.any(Employee.id == int(emp_id))).all()
#         # data_schema = AttendenceSchema(many=True)
#         today = datetime.now()
#         today.year()
#         return jsonify(json_data)
#     else:
#         return jsonify({'message': 'Invalid HTTP request method.'})


@bp.route('/attendence/summary/latecomin', methods=['POST'])
def summary_late_attendence():
    if request.method == "POST":
        # Setting fiscal Year
        today = datetime.now()
        payload_date = datetime(
            int(today.year), int(1), int(1))
        payload_date_end = datetime(
            int(today.year + 1), int(1), int(1))
        all_emps = Employee.query.filter(Employee.flag == 0).all()
        payload = {}
        payload_late = {}
        payload_early = {}
        for emp in all_emps:
            data = Attendence.query.filter(Attendence.employee.any(Employee.id == int(emp.id)),
                                           Attendence.date >= payload_date, Attendence.date <= payload_date_end).all()

            day_att = 0
            early_att = 0
            late_att = 0
            for item in data:
                day_att += item.daysatt
                early_att += item.earlygoing
                late_att += item.latecomin
            company_schema = CompanySchema(many=True) 
            payload_data = {'name': emp.name, 'company': company_schema.dumps(emp.company), 'day_att': day_att, 'early_att': early_att, 'late_att': late_att}
            payload_late.update({emp.id: payload_data})
        payload_late = sorted(payload_late.items(), key = lambda x : x[1]['late_att'])[::-1][:5]
        payload_early = sorted(payload_early.items(), key = lambda x : x[1]['early_att'])[::-1][:5]
        payload['early'] = payload_early
        payload['late'] = payload_late
        return jsonify(payload)
    else:
        return jsonify({'message': 'Invalid HTTP request method.'})


@bp.route('/attendence/save', methods = ['POST'])
def save_attendence():
    if request.method == 'POST':
        payload=request.json
        if payload != None:
            payload_data=payload['data']
            payload_date=payload['date'].split('-')
            payload_date=datetime(
                int(payload_date[0]), int(payload_date[1]), int(1))
            # Date checks to be done
            table_columns=(
                'daysatt',
                'latecomin',
                'earlygoing'

            )
            try:

                # Need Update cehck inside
                for item in payload_data:
                    new_data=Attendence()
                    emp=Employee.query.filter_by(
                        id = int(item['id'])).first()
                    company=Company.query.filter_by(
                        id = int(payload['company'])).first()
                    new_data.company.append(company)
                    new_data.employee.append(emp)
                    for field in table_columns:
                        val=item[field]
                        if val == '' or val is None:
                            continue
                        setattr(new_data, field, val)
                    setattr(new_data, 'date', payload_date)

                    if 'tdsval' in item.keys():
                        if item['tdsval'] != "":
                            setattr(new_data, 'tds', item['tdsval'])

                    if 'other_deduction' in item.keys():
                        val=item['other_deduction']
                        if val == '' or val is None:
                            continue
                        setattr(new_data, 'other_deduction',
                                item['other_deduction'])

                    if 'esival' in item.keys():
                        if item['esival'] != "":

                            setattr(new_data, 'esi', item['esival'])

                    if 'pfval' in item.keys():
                        if item['pfval'] != "":
                            setattr(new_data, 'pf', item['pfval'])

                db.session.add(new_data)
                db.session.commit()
                return jsonify({'success': 'Data Added'})

            except Exception as e:
                db.session.rollback()
                return jsonify({'message': 'Something went wrong'})

            return jsonify({'message': 'Something went wrong'})
        else:
            return jsonify({'message': 'Empty data.'})


@bp.route('/attendence/update', methods = ['POST'])
def update_attendence():
    if request.method == 'POST':
        payload=request.json
        if payload != None:

            table_columns=(
                'daysatt',
                'latecomin',
                'earlygoing'
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

                    if 'other_deduction' in item.keys():
                        val = item['other_deduction']
                        if val == '' or val is None:
                            continue
                        setattr(saved_att, 'other_deduction',
                                item['other_deduction'])

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

                db.session.commit()
                return jsonify({'success': 'Data Updated'})

            except Exception as e:
                print(str(e))
                db.session.rollback()
                return jsonify({'message': 'Something went wrong'})

            return jsonify({'message': 'Something went wrong'})
        else:
            return jsonify({'message': 'Empty data.'})

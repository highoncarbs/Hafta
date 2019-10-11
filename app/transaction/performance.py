from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_required
from app.transaction import bp
from app.employee.model import Employee, EmployeeAdvanceSchema
from app.master.model import Company, Performance, PerformanceSchema
from app.transaction.model_per import PerformanceItem, TransPerformance, TransPerformanceSchema
from app import db, ma
from datetime import datetime

import json


@bp.route('/performance', methods=['GET'])
@login_required
def show_performance():
    return render_template('transaction/performance.html')


@bp.route('/get/performance', methods=['GET'])
@login_required
def get_performance_factors():
    data_schema = PerformanceSchema(many=True)
    data = Performance.query.all()
    json_data = data_schema.dumps(data)
    return jsonify(json_data)


@bp.route('/performance/all', methods=['POST'])
@login_required
def get_performance_all():

    data_schema = TransPerformanceSchema(many=True)
   
    data = TransPerformance.query.all()

    json_data = json.loads(data_schema.dumps(data))
    factors = Performance.query.all()

    for item in json_data:
        item['net_score'] = float(0)
        max_score = float(0)

        for prf_item in item['performance_items']:

            for fac in factors:

                if fac.id == prf_item['performance_id']:
                    max_score += float(fac.score)*float(fac.weight)
                    item['net_score'] += float(prf_item['obt_score']
                                               )*float(fac.weight)

        item['net_score'] = float(item['net_score']/max_score)*100
        item['net_score'] = "%.2f" % round(item['net_score'], 2)

    json_data = json.dumps(json_data)
    return jsonify(json_data)


@bp.route('/performance/company', methods=['POST'])
@login_required
def get_performance_factors_for_emp():
    if request.method == 'POST':

        data_schema = TransPerformanceSchema(many=True)
        payload = request.json
        temp_date = payload['fromdate'].split('-')
        fromdate = datetime(
            int(temp_date[0]), int(temp_date[1]), int(temp_date[2]))

        temp_date = payload['todate'].split('-')
        todate = datetime(
            int(temp_date[0]), int(temp_date[1]), int(temp_date[2]))

        data = TransPerformance.query.join(TransPerformance.employee).join(Employee.company).filter(
            Company.id == int(payload['company']), TransPerformance.fromdate >= fromdate, TransPerformance.todate <= todate).all()

        json_data = json.loads(data_schema.dumps(data))
        factors = Performance.query.all()

        for item in json_data:
            item['net_score'] = float(0)
            max_score = float(0)

            for prf_item in item['performance_items']:

                for fac in factors:

                    if fac.id == prf_item['performance_id']:
                        max_score += float(fac.score)*float(fac.weight)
                        item['net_score'] += float(prf_item['obt_score']
                                                   )*float(fac.weight)
            if(max_score != float(0)):
                item['net_score'] = float(item['net_score']/max_score)*100
                item['net_score'] = "%.2f" % round(item['net_score'], 2)
            
            else :
                item['net_score'] = 0
        
        json_data = json.dumps(json_data)
        return jsonify(json_data)


@bp.route('/performance/get/employee/<id>', methods=['GET'])
@login_required
def get_performance_by_employee(id):
    data_schema = TransPerformanceSchema(many=True)
    data = TransPerformance.query.filter_by(emp_id=int(id)).all()
    json_data = data_schema.dumps(data)
    return jsonify(json_data)


@bp.route('/performance/save', methods=['POST'])
@login_required
def save_performance():
    if request.method == 'POST':
        payload = request.json
        if payload is not None:

            emp = Employee.query.filter_by(id=int(payload['emp_id'])).first()

            temp_date = payload['fromdate'].split('-')
            fromdate = datetime(
                int(temp_date[0]), int(temp_date[1]), int(temp_date[2]))

            temp_date = payload['todate'].split('-')
            todate = datetime(
                int(temp_date[0]), int(temp_date[1]), int(temp_date[2]))

            payload_data = payload['data']

            check_data = TransPerformance.query.filter_by(emp_id=int(
                payload['emp_id']), fromdate=fromdate, todate=todate)

            if check_data.first() is None:
                new_data = TransPerformance(
                    int(payload['emp_id']), fromdate, todate)
                for item in payload_data:
                    factor = Performance.query.filter_by(
                        id=int(item['id'])).first()
                    new_data.performance_items.append(
                        PerformanceItem(factor, item['obt_score']))
                new_data.employee.append(emp)

                try:
                    db.session.add(new_data)
                    db.session.commit()
                    return jsonify({'success': 'Data added'})

                except Exception as e:
                    return jsonify({'message': 'Something went wrong - '+str(e)})

            else:
                return jsonify({'message': 'Data already exists'})
        else:
            return jsonify({'message': 'Empty data'})
    return jsonify({'message': 'Invalid HTTP Method. Use POST instead'})


@bp.route('/performance/delete/<perf_id>', methods=['POST'])
def delete_performance(perf_id):
    data = TransPerformance.query.filter_by(id=int(perf_id))
    if data.first() is None:
        return jsonify({'message': 'Could not find advance transaction'})
    else:
        try:
            data.employee = []
            data.performance_items = []
            data.delete()
            db.session.commit()
            return jsonify({'success': 'Performance transaction deleted'})
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Something went wrong .'})


@bp.route('/performance/update', methods=['POST'])
def update_performance():
    payload = request.json
    if payload is not None:
        data = TransPerformance.query.filter_by(id=int(payload['id'])).first()
        if data is None:
            return jsonify({'message': 'Could not find advance transaction'})
        else:
            try:
                data.performance_items = []
                db.session.commit()

                # Updated the new Obt_score

                for item in payload['performance_items']:
                    factor = Performance.query.filter_by(
                        id=int(item['performance_id'])).first()
                    data.performance_items.append(
                        PerformanceItem(factor, item['obt_score']))

                db.session.commit()
                return jsonify({'success': 'Performance transaction updated'})
            except Exception as e:
                print(str(e))
                return jsonify({'message': 'Something went wrong .'})
    else:
        return jsonify({'message': 'Invalid HTTP request .'})

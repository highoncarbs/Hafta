# Salary Sheet


from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user
from app.transaction import bp
from app.employee.model import Employee, EmployeeAdvanceSchema
from app.master.model import Company, AttendenceRules
from app.transaction.model_att import Attendence, AttendenceSchema
from app.transaction.model_adv import Advance, AdvanceSchema
from app.transaction.model_sal import SalarySheet, SalarySheetSlips
from app import db, ma
from datetime import datetime
import requests
import json



@bp.route('/salary_sheet/', methods=['GET'])
def show_sheet():
    return render_template('transaction/salary_sheet.html')


@bp.route('/salary_sheet/print/all', methods=['GET', 'POST'])
def print_salatry_sheet_company():
    return render_template('reports/print_sheet.html')


@bp.route('/salary_sheet/delete/<id>', methods=['GET', 'POST'])
def delete_salatry_sheet_company(id):
    data = SalarySheet.query.filter_by(id=int(id))
    try:
        data.delete()
        db.session.commit()

        return jsonify({'success' : 'Deleted'})
    except Exception as e:
        return jsonify({'message' : 'Somethign went wrong' + str(e)})

@bp.route('/salary_sheet/print/selected', methods=['GET', 'POST'])
def print_salatry_sheet_selected():
    return render_template('reports/print_sheet_selected.html')


@bp.route('/salary_sheet/slips', methods=['POST'])
def salary_slips_emp():
    # Needs none checks
    payload = request.json
    if payload is not None:
        payload_date = payload['date'].split('-')
        payload_date = datetime(
            int(payload_date[0]), int(payload_date[1]), int(1))
        emp_id = payload['emp_id']
        json_schema = AttendenceSchema()

        emp_att = Attendence.query.filter(Attendence.employee.any(
            Employee.id == int(emp_id)), Attendence.date == payload_date).first()
            
        slips = SalarySheetSlips.query.filter(SalarySheetSlips.employee.any(
            Employee.id == int(emp_id)), SalarySheetSlips.date == payload_date).first()
        if slips is not None and emp_att is not None:
            json_data = json.loads(json_schema.dumps(emp_att))
            att_rules = AttendenceRules.query.first()
            late_comin_ratio = float(
                att_rules.late_comin_day / att_rules.late_comin)
            early_going_ratio = float(
                att_rules.early_going_day / att_rules.early_going)

            json_data['net_adv_deduction'] = slips.adv_deduction

            json_data['days_payable_late'] = late_comin_ratio * \
                json_data['latecomin']

            json_data['days_payable_early'] = early_going_ratio * \
                json_data['earlygoing']
            json_data['days_payable'] = round(
                json_data['daysatt'] - (json_data['days_payable_late'] + json_data['days_payable_early']), 2)

            json_data['pay_1'] = float(
                json_data['days_payable']) * (float(json_data['employee'][0]['basicpay']) / 30)

            if json_data['esi'] is None:
                json_data['esi'] = 0
            if json_data['tds'] is None:
                json_data['tds'] = 0
            if json_data['pf'] is None:
                json_data['pf'] = 0

            if json_data['other_deduction'] is None:
                json_data['other_deduction'] = 0

            json_data['total_deductions'] = float(json_data['esi']) + float(json_data['pf']) + float(
                json_data['tds']) + float(json_data['other_deduction']) + float(json_data['net_adv_deduction'])

            json_data['net_payable'] = float(
                json_data['pay_1'] - json_data['total_deductions'])
            return jsonify({'success': json_data})
        else:
            return jsonify({'message': 'Data not present'})
    else:
        return jsonify({'message': 'Empty data recieved.'})

@bp.route('/salary_sheet/slips/range', methods=['POST'])
def salary_slips_emp_range():
    # Needs none checks
    payload = request.json
    if payload is not None:
        payload_start_date = payload['start_date'].split('-')
        payload_start_date = datetime(
            int(payload_start_date[0]), int(payload_start_date[1]), int(1))
        
        payload_end_date = payload['end_date'].split('-')
        payload_end_date = datetime(
            int(payload_end_date[0]), int(payload_end_date[1]), int(1))
        
        emp_id = payload['emp_id']
        json_schema = AttendenceSchema()

        emp_att = Attendence.query.filter(Attendence.employee.any(
            Employee.id == int(emp_id)), Attendence.date >= payload_start_date , Attendence.date <= payload_end_date).all()

        slips = SalarySheetSlips.query.filter(SalarySheetSlips.employee.any(
            Employee.id == int(emp_id)), SalarySheetSlips.date >= payload_start_date , SalarySheetSlips.date <= payload_end_date ).all()
        
        print(slips)
        
        
        att_rules = AttendenceRules.query.first()
        
        late_comin_ratio = float(
        att_rules.late_comin_day / att_rules.late_comin)
        
        early_going_ratio = float(
        att_rules.early_going_day / att_rules.early_going)
        
        all_data = []
        
        for slip, att in zip(slips , emp_att):
        
            json_data = json.loads(json_schema.dumps(att))
            

            json_data['net_adv_deduction'] = slip.adv_deduction

            json_data['days_payable_late'] = late_comin_ratio * \
                json_data['latecomin']

            json_data['days_payable_early'] = early_going_ratio * \
                json_data['earlygoing']

            json_data['days_payable'] = round(
                json_data['daysatt'] - (json_data['days_payable_late'] + json_data['days_payable_early']), 2)

            json_data['pay_1'] = float(
                json_data['days_payable']) * (float(json_data['employee'][0]['basicpay']) / 30)

            if json_data['esi'] is None:
                json_data['esi'] = 0
            if json_data['tds'] is None:
                json_data['tds'] = 0
            if json_data['pf'] is None:
                json_data['pf'] = 0

            if json_data['other_deduction'] is None:
                json_data['other_deduction'] = 0

            json_data['total_deductions'] = float(json_data['esi']) + float(json_data['pf']) + float(
                json_data['tds']) + float(json_data['other_deduction']) + float(json_data['net_adv_deduction'])

            json_data['net_payable'] = float(
                json_data['pay_1'] - json_data['total_deductions'])
            print(json_data['net_payable'])
            all_data.append(json_data)
        return jsonify({'success': all_data})
    else:
        return jsonify({'message': 'Data not present'})
 
@bp.route('/salary_sheet/process', methods=['POST'])
def process_sheet():
    payload = request.json
    if payload is not None:
        json_data = payload['data']
        payload_company = Company.query.filter_by(
            id=int(payload['company'])).first()
        payload_date = payload['date'].split('-')
        payload_date = datetime(
            int(payload_date[0]), int(payload_date[1]), int(1))

        net_paid = float(0)
        net_advance_deduction = float(0)
        net_attendence = {}

        check_data = SalarySheet.query.filter(SalarySheet.company.any(Company.id == int(payload['company'])),
                                              SalarySheet.month == payload_date)
        if check_data.first() is None:
            salary = SalarySheet(
                payload_date, net_advance_deduction, net_paid, json.dumps(net_attendence))
            for item in json_data:
                # Debit advance
                try:
                    emp = Employee.query.filter_by(
                        id=int(item['employee'][0]['id'])).first()
                    slip_data = SalarySheetSlips(
                        item['net_adv_deduction'], payload_date)
                    slip_data.employee.append(emp)
                    pending_advance = float(
                        item['net_deduction_month']) + float(item['net_deduction_year'])
                    if pending_advance is not float(0):
                        new_data = Advance(advanceamt=float(
                            item['net_adv_deduction']), trans="debit", date=payload_date, deduction_period="debit")
                        new_data.employee.append(emp)
                        new_data.employee.append(payload_company)
                        db.session.add(new_data)

                    slip_data.sheet.append(salary)

                    db.session.add(slip_data)
                    db.session.commit()
                    net_paid += float(item['net_payable'])
                    net_advance_deduction += float(item['net_adv_deduction'])
                # Attendece Percentage later
                except Exception as e:
                    print(str(e))
                    return jsonify({'message': 'Something went wrong. -'+str(e)})

            try:

                salary.company.append(payload_company)

                db.session.add(salary)
                db.session.commit()
                return jsonify({'success': 'Payroll processed.'})

            except Exception as e:
                print(str(e))
                return jsonify({'message': 'Something went wrong. -'+str(e)})
        else:
            return jsonify({'message': 'Salary Sheet already processed fo this month.'})

        # Save payroll info - paid out , advances paid out ,deductions & attendence
    else:
        return jsonify({'message': 'Empty data recieved.'})


@bp.route('/salary_sheet/generate', methods=['POST'])
def salary_generate_sheet():
    if request.method == 'POST':
        if request.json != None:
            try:
                payload = request.json
                company = payload['company']
                month = payload['month']
                return generate_sheet(company, month)
            except Exception as e:
                print(str(e))
                return jsonify({'message': 'Data not entered for required company & month.'})


@bp.route('/salary_sheet/get/processed', methods=['POST'])
def get_processed_sheet():

    payload = request.json
    if payload is not None:

        payload_date = payload['date'].split('-')
        payload_date = datetime(
            int(payload_date[0]), int(payload_date[1]), int(1))

        check_data = SalarySheet.query.filter(SalarySheet.company.any(Company.id == int(payload['company'])),
                                              SalarySheet.month == payload_date).first()
        if check_data is not None:
            saved_data = SalarySheetSlips.query.filter(
                SalarySheetSlips.sheet.any(SalarySheet.id == int(check_data.id))).all()
            try:

                generate_data = json.loads(generate_sheet(
                    payload['company'], payload['date']).data)
                for item in generate_data:
                    for slip in saved_data:
                        if (item['employee'][0]['id'] == slip.employee[0].id):
                            item['net_adv_deduction'] = slip.adv_deduction

                json_data = json.dumps(generate_data)
                return jsonify({'data': json_data})
            except Exception as e:
                print(str(e))
                return jsonify({'message': 'Data not entered for required company & month.'})
        else:
            return jsonify({'data': None})


def generate_sheet(company, month):
    # Payload Date from User

    payload_date = month.split('-')
    payload_date = datetime(
        int(payload_date[0]), int(payload_date[1]), int(1))

    # Attendence data for company and month
    att_data = Attendence.query.filter(
        Attendence.company.any(Company.id == int(company)), Attendence.date == payload_date).all()

    # For year range
    today = payload_date
    year_start = datetime(today.year, 1, 1)
    year_end = datetime(today.year+1, 1, 1)

    att_data_schema = AttendenceSchema(many=True)
    json_att_data = json.loads(att_data_schema.dumps(att_data))
    adv_data_schema = AdvanceSchema(many=True)

    att_rules = AttendenceRules.query.first()
    late_comin_ratio = float(
        att_rules.late_comin_day / att_rules.late_comin)
    early_going_ratio = float(
        att_rules.early_going_day / att_rules.early_going)

    for att_item in json_att_data:
        att_item['advance'] = []
        att_item['deductions'] = {}
        att_item['deductions']['month'] = []

        att_item['days_payable_late'] = late_comin_ratio * \
            att_item['latecomin']
        att_item['days_payable_early'] = early_going_ratio * \
            att_item['earlygoing']

        att_item['days_payable'] = round(
            att_item['daysatt'] - (att_item['days_payable_late'] + att_item['days_payable_early']), 2)

        att_item['pay_1'] = float(
            att_item['days_payable']) * (float(att_item['employee'][0]['basicpay']) / 30)

        att_item['deductions']['year'] = []

        # Includes deduction from the month
        adv_data = Advance.query.filter(
            Advance.employee.any(Employee.id == int(att_item['employee'][0]['id']))).all()
        json_adv_data = json.loads(adv_data_schema.dumps(adv_data))
        net_advance_month = 0
        net_advance_year = 0
        net_deduction_month = 0
        net_deduction_year = 0

        outstanding_advance = float(0)

        for item in adv_data:
            if (item.trans == 'credit'):
                outstanding_advance += float(item.advanceamt)

            elif (item.trans == 'debit'):
                outstanding_advance -= float(item.advanceamt)

        for adv_item in json_adv_data:
            if adv_item['deduction_period'] == 'month':

                net_advance_month += float(adv_item['advanceamt'])
                net_deduction_month += float(adv_item['deduction'])

                # net_advance += float(-100)
                att_item['deductions']['month'].append(
                    adv_item['deduction'])

            if adv_item['deduction_period'] == 'year':
                if payload_date.month is 12:

                    net_advance_year += float(adv_item['advanceamt'])
                    net_deduction_year += float(adv_item['deduction'])

                    # net_advance += float(-100)

                    att_item['deductions']['year'].append(
                        adv_item['deduction'])

        if net_advance_month > net_deduction_month:
            pass
        elif net_advance_month <= net_deduction_month:
            att_item['deductions']['month'] = [ net_advance_month ]

        if net_advance_year > net_deduction_year:
            pass
        elif net_advance_year <= net_deduction_year:
            att_item['deductions']['year'] = [ net_advance_year ]

        # Setting to 0 if balance is 0

        if float(net_advance_month) is float(0):
            att_item['deductions']['month'] = 0
            att_item['deductions']['month'] = 0
        if float(net_advance_year) is float(0):
            att_item['deductions']['year'] = 0
            att_item['deductions']['year'] = 0

        if att_item['other_deduction'] is None:
            att_item['other_deduction'] = float(0)
        if att_item['esi'] is None:
            att_item['esi'] = float(0)
        if att_item['pf'] is None:
            att_item['pf'] = float(0)
        if att_item['tds'] is None:
            att_item['tds'] = float(0)

        att_item['net_deduction_month'] = float(net_deduction_month)
        att_item['net_deduction_year'] = float(net_deduction_year)

        net_deduction_advance = float(
            net_deduction_month) + float(net_deduction_year)

        if outstanding_advance <= net_deduction_advance:
            att_item['net_adv_deduction'] = outstanding_advance
        else:
            att_item['net_adv_deduction'] = net_deduction_advance

        att_item['total_deductions'] = float(net_deduction_month) + float(att_item['esi']) + float(att_item['pf']) + float(
            att_item['tds'])+float(att_item['other_deduction']) + float(att_item['net_deduction_year'])
        att_item['net_payable'] = float(
            att_item['pay_1'] - att_item['total_deductions'])
    return jsonify(json_att_data)

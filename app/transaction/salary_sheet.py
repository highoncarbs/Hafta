# Salary Sheet


from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user
from app.transaction import bp
# from app.transaction.model_sal im
from app.employee.model import Employee, EmployeeAdvanceSchema
from app.master.model import Company, AttendenceRules
from app.transaction.model_att import Attendence, AttendenceSchema
from app.transaction.model_adv import Advance, AdvanceSchema

from app import db, ma
from datetime import datetime

import json
@bp.route('/salary_sheet/', methods=['GET'])
def show_sheet():
    return render_template('transaction/salary_sheet.html')


@bp.route('/salary_sheet/generate', methods=['POST'])
def generate_sheet():
    if request.method == 'POST':
        if request.json != None:
            payload = request.json
            company = payload['company']
            month = payload['month']

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
                att_item['days_payable_late'] = late_comin_ratio *  att_item['latecomin']
                att_item['days_payable_early'] = early_going_ratio * att_item['earlygoing']
                
                att_item['days_payable'] = round(att_item['daysatt'] - ( att_item['days_payable_late'] + att_item['days_payable_early']) , 2)

                att_item['pay_1'] = float(att_item['days_payable'])* (float(att_item['employee'][0]['basicpay']) / 30)  

                att_item['deductions']['year'] = []

                adv_data = Advance.query.filter(
                    Advance.employee.any(Employee.id == int(att_item['employee'][0]['id'])), Advance.date >= year_start, Advance.date <= year_end, Advance.date >= payload_date).all()
                json_adv_data = json.loads(adv_data_schema.dumps(adv_data))

                net_advance_month = 0
                net_advance_year = 0
                net_deduction_month = 0
                net_deduction_year = 0
                for adv_item in json_adv_data:
                    if payload_date.month is not 12:
                        if adv_item['deduction_period'] == 'month':

                            net_advance_month += float(adv_item['advanceamt'])
                            net_deduction_month += float(adv_item['deduction'])

                            # net_advance += float(-100)
                            att_item['deductions']['month'].append(
                                adv_item['deduction'])

                    else:
                        if adv_item['deduction_period'] == 'year':

                            net_advance_year += float(adv_item['advanceamt'])
                            net_deduction_year += float(adv_item['deduction'])

                            # net_advance += float(-100)

                            att_item['deductions']['year'].append(
                                adv_item['deduction'])

                if net_advance_month > net_deduction_month:
                    pass
                elif net_advance_month <= net_deduction_month:
                    att_item['deductions']['month'] = net_advance_month

                if float(net_advance_month) is float(0):
                    att_item['deductions']['month'] = 0
                    att_item['deductions']['month'] = 0

                if net_advance_year > net_deduction_year:
                    pass
                elif net_advance_year <= net_deduction_year:
                    att_item['deductions']['year'] = net_advance_year

                if float(net_advance_year) is float(0):
                    att_item['deductions']['year'] = 0
                    att_item['deductions']['year'] = 0
                
                print(net_deduction_month , att_item['esi'] , att_item['pf'] , att_item['tds'] , att_item['other_deduction'])
                if att_item['other_deduction'] is None:
                    att_item['other_deduction'] = float(0)
                if att_item['esi'] is None:
                    att_item['esi'] = float(0)
                if att_item['pf'] is None:
                    att_item['pf'] = float(0)
                if att_item['tds'] is None:
                    att_item['tds'] = float(0)
                
                att_item['total_deductions'] = float(net_deduction_month) + float(att_item['esi']) +float(att_item['pf']) +float(att_item['tds'])+float(att_item['other_deduction'])
                att_item['net_payable'] =  float(att_item['pay_1'] - att_item['total_deductions'])

        return jsonify(json_att_data)

from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user
from app.master import bp
from app.master.model import AttendenceRules , AttendenceRuleSchema
from app import db, ma


# Emp. Cat Master Routes


@bp.route('/get/attendence_rules', methods=['GET'])
def get_attendence_rules():
    if request.method == 'GET':
        data_schema = AttendenceRuleSchema(many=True)
        data = AttendenceRules.query.all()
        json_data = data_schema.dump(data)
        return jsonify(json_data)


@bp.route('/add/attendence_rules', methods=['POST'])
def add_attendence_rules():
    if request.method == 'POST':
        payload = request.json
        if payload is not None:

            check_data = AttendenceRules.query
            if check_data.first():
                return jsonify({'message': 'Only one Rule is allowed , please edit or delete existing rule.'})
            else:
                try:
                    new_data = AttendenceRules(payload['late_comin'] , payload['late_comin_day'], payload['early_going'] , payload['early_going_day'])
                    db.session.add(new_data)
                    db.session.commit()
                    return jsonify({'success': 'Rule Added'})

                except Exception as e:
                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Empty Data.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})


@bp.route('/edit/attendence_rules', methods=['POST'])
def edit_attendence_rules():
    if request.method == 'POST':
        payload = request.json
        if payload is not None:

            check_data = AttendenceRules.query.filter_by(id=int(payload['id']) )
            if check_data.first():
                try:
                    new_data = check_data.first()
                    new_data.late_comin = payload['late_comin']
                    new_data.early_going = payload['early_going']
                    new_data.late_comin_day = payload['late_comin_day']
                    new_data.early_going_day = payload['early_going_day']
                    
                    db.session.commit()
                    return jsonify({'success': 'Data Updated'})

                except Exception as e:
                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Empty Data.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})


@bp.route('/delete/attendence_rules', methods=['POST'])
def delete_attendence_rules():
    if request.method == 'POST':
        payload = request.json
        check_data = AttendenceRules.query.filter_by(id=payload['id'])
        if check_data.first():
            try:
                check_data.delete()
                db.session.commit()
                return jsonify({'success': 'Data deleted'})
            except Exception as e:
                db.session.rollback()
                db.session.close()
                return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Data does not exist.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})

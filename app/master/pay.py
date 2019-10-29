from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user
from app.master import bp
from app.master.model import ModeOfPay, PaySchema
from app import db, ma


# Emp. Cat Master Routes


@bp.route('/get/pay', methods=['GET'])
def get_pay():
    if request.method == 'GET':
        data_schema = PaySchema(many=True)
        data = ModeOfPay.query.all()
        json_data = data_schema.dump(data)
        return jsonify(json_data)


@bp.route('/add/pay', methods=['POST'])
def add_pay():
    if request.method == 'POST':
        payload = request.json
        if payload['name'] is not None:

            check_data = ModeOfPay.query.filter_by(name=payload['name'])
            if check_data.first():
                return jsonify({'message': 'ModeOfPay - '+check_data.first().name+' already exists.'})
            else:
                try:
                    new_data = ModeOfPay(payload['name'])
                    db.session.add(new_data)
                    db.session.commit()
                    return jsonify({'success': 'Data Added'})

                except Exception as e:
                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Empty Data.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})


@bp.route('/edit/pay', methods=['POST'])
def edit_pay():
    if request.method == 'POST':
        payload = request.json
        if payload['name'] is not None:

            check_data = ModeOfPay.query.filter_by(name=payload['name'])
            if check_data.first():
                return jsonify({'message': 'Mode of Pay - '+check_data.first().name+' already exists.'})
            else:
                try:
                    new_data = ModeOfPay.query.filter_by(
                        id=payload['id']).first()
                    new_data.name = payload['name']
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


@bp.route('/delete/pay', methods=['POST'])
def delete_pay():
    if request.method == 'POST':
        payload = request.json
        check_data = ModeOfPay.query.filter_by(id=payload['id'])
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

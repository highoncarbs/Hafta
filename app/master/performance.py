from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user
from app.master import bp
from app.master.model import Performance, PerformanceSchema
from app import db, ma


# Emp. Cat Master Routes


@bp.route('/get/performance', methods=['GET'])
def get_perfomance():
    if request.method == 'GET':
        data_schema = PerformanceSchema(many=True)
        data = Performance.query.all()
        json_data = data_schema.dump(data)
        return jsonify(json_data)


@bp.route('/add/performance', methods=['POST'])
def add_perfomance():
    if request.method == 'POST':
        payload = request.json
        if payload['name'] is not None:

            check_data = Performance.query.filter_by(name=payload['name'])
            if check_data.first():
                return jsonify({'message': 'Performance - '+check_data.first().name+' already exists.'})
            else:
                try:
                    new_data = Performance(payload['name'] ,payload['score'] , payload['weight'] )
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


@bp.route('/edit/performance', methods=['POST'])
def edit_perfomance():
    if request.method == 'POST':
        payload = request.json
        if payload['name'] is not None:

            check_data = Performance.query.filter_by(name=payload['name'])
            if not check_data.first():
                try:
                    new_data = Performance.query.filter_by(
                        id=payload['id']).first()
                    new_data.name = payload['name']
                    new_data.score = payload['score']
                    new_data.weight = payload['weight']
                    db.session.commit()
                    return jsonify({'success': 'Data Updated'})

                except Exception as e:
                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
            else:
                return jsonify({'message': 'Duplicate Data'})
        else:
            return jsonify({'message': 'Empty Data.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})


@bp.route('/delete/performance', methods=['POST'])
def delete_perfomance():
    if request.method == 'POST':
        payload = request.json
        check_data = Performance.query.filter_by(id=payload['id'])
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

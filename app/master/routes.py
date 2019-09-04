from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user
from app.master import bp
from app.master.model import Company, Location, LocationSchema , CompanySchema
from app import db, ma


@bp.route('/', methods=['GET'])
def view_master():
    return render_template('master/master.html')
#  Company Master Routes
@bp.route('/get/company', methods=['GET'])
def view_company():
    if request.method == 'GET':
        data_schema = CompanySchema(many=True)
        data = Company.query.all()
        json_data = data_schema.dump(data)
        print(json_data)
        return jsonify(data_schema.dump(data))

@bp.route('/add/company', methods=['POST'])
def add_company():
    if request.method == 'POST':
        payload = request.json
        if payload['name'] and payload['location'] is not None:

            check_data = Company.query.filter_by(name=payload['name'])
            if check_data.first():
                return jsonify({'message': 'Company - '+check_data.first().name+' already exists.'})
            else:
                try:
                    new_data = Company(payload['name'])
                    location = Location.query.filter_by(
                        id=payload['location']).first()
                    print(location)
                    new_data.location.append(location)
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


@bp.route('/edit/company', methods=['POST'])
def edit_company():
    if request.method == 'POST':
        payload = request.json
        if payload['name'] and payload['location'] is not None:
            location = Location.query.filter_by(
                        id=payload['location']).first()
            data_schema = LocationSchema()
            json_data = data_schema.dump(location)
            check_data = Company.query.filter_by(id=payload['id'])
            if check_data.first():
                
                try:
                    new_data = Company.query.filter_by(
                        id=payload['id']).first()
                    new_data.name = payload['name']
                    new_data.location.clear()
                    new_data.location.append(location)

                    db.session.commit()
                    
                    return jsonify({'success': 'Data Updated' , 'payload' : json_data})

                except Exception as e:
                    db.session.rollback()
                    db.session.close()
                    print(e)
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Empty Data.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})


@bp.route('/delete/company', methods=['POST'])
def delete_company():
    if request.method == 'POST':
        payload = request.json

        check_data = Company.query.filter_by(name=payload['name'])
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

# Location Master Routes


@bp.route('/get/location', methods=['GET'])
def get_location():
    if request.method == 'GET':
        data_schema = LocationSchema(many=True)
        data = Location.query.all()
        json_data = data_schema.dump(data)
        return jsonify(json_data)


@bp.route('/add/location', methods=['POST'])
def add_location():
    if request.method == 'POST':
        payload = request.json
        if payload['name'] is not None:

            check_data = Location.query.filter_by(name=payload['name'])
            if check_data.first():
                return jsonify({'message': 'Location - '+check_data.first().name+' already exists.'})
            else:
                try:
                    new_data = Location(payload['name'])
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


@bp.route('/edit/location', methods=['POST'])
def edit_location():
    if request.method == 'POST':
        payload = request.json
        if payload['name'] is not None:

            check_data = Location.query.filter_by(name=payload['name'])
            if check_data.first():
                return jsonify({'message': 'Location - '+check_data.first().name+' already exists.'})
            else:
                try:
                    new_data = Location.query.filter_by(
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


@bp.route('/delete/location', methods=['POST'])
def delete_location():
    if request.method == 'POST':
        payload = request.json
        print(payload)
        check_data = Location.query.filter_by(id=payload['id'])
        if check_data.first():
            try:
                print(check_data.first().name)
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

from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user , login_required
from app.master import bp
from app.master.model import Company, Location, LocationSchema, CompanySchema, EmployeeCategory, EmployeeCatSchema
from app import db, ma
from sqlalchemy.exc import IntegrityError


@bp.route('/', methods=['GET'])
@login_required
def view_master():
    return render_template('master/master.html')

    
#  Company Master Routes
@bp.route('/get/company', methods=['GET'])
@login_required
def view_company():
    if request.method == 'GET':
        data_schema = CompanySchema(many=True)
        data = Company.query.all()
        return jsonify(data_schema.dump(data))


@bp.route('/add/company', methods=['POST'])
@login_required
def add_company():
    if request.method == 'POST':
        payload = request.json
        if payload['name'] and payload['location'] is not None:

                try:
                    location = Location.query.filter_by(
                        id=payload['location']).first()
                    new_data = Company(payload['name'] , location.id)
                    new_data.location.append(location)
                    db.session.add(new_data)
                    db.session.commit()
                    return jsonify({'success': 'Data Added'})
                except IntegrityError as e:
                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Duplicate Entry'})

                except Exception as e:
                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Empty Data.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})


@bp.route('/edit/company', methods=['POST'])
@login_required
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

                    return jsonify({'success': 'Data Updated', 'payload': json_data})

                except Exception as e:
                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Empty Data.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})


@bp.route('/delete/company', methods=['POST'])
@login_required
def delete_company():
    if request.method == 'POST':
        payload = request.json

        check_data = Company.query.filter_by(name=payload['name'])
        if check_data.first():
            try:

                if(len(check_data.first().emp_company) != 0):
                    return jsonify({'message': 'Cannot delete , data being used. '})
                else:
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
@login_required
def get_location():
    if request.method == 'GET':
        data_schema = LocationSchema(many=True)
        data = Location.query.all()
        json_data = data_schema.dump(data)
        return jsonify(json_data)


@bp.route('/add/location', methods=['POST'])
@login_required
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
@login_required
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
@login_required
def delete_location():
    if request.method == 'POST':
        payload = request.json
        check_data = Location.query.filter_by(id=payload['id'])
        if check_data.first():
            if len(check_data.first().company_location) is int(0):

                try:
                    check_data.delete()
                    db.session.commit()
                    return jsonify({'success': 'Data deleted'})
                except Exception as e:
                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
            else:
                return jsonify({'message': 'Cannot delete data. Being used by other master.'})

        else:
            return jsonify({'message': 'Data does not exist.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})

# Emp. Cat Master Routes


@bp.route('/get/cat', methods=['GET'])
@login_required
def get_cat():
    if request.method == 'GET':
        data_schema = EmployeeCatSchema(many=True)
        data = EmployeeCategory.query.all()
        json_data = data_schema.dump(data)
        return jsonify(json_data)


@bp.route('/add/cat', methods=['POST'])
@login_required
def add_cat():
    if request.method == 'POST':
        payload = request.json
        if payload['name'] is not None:

            check_data = EmployeeCategory.query.filter_by(name=payload['name'])
            if check_data.first():
                return jsonify({'message': 'Emp. Category - '+check_data.first().name+' already exists.'})
            else:
                try:
                    new_data = EmployeeCategory(payload['name'])
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


@bp.route('/edit/cat', methods=['POST'])
@login_required
def edit_cat():
    if request.method == 'POST':
        payload = request.json
        if payload['name'] is not None:

            check_data = EmployeeCategory.query.filter_by(name=payload['name'])
            if check_data.first():
                return jsonify({'message': 'Emp. Category - '+check_data.first().name+' already exists.'})
            else:
                try:
                    new_data = EmployeeCategory.query.filter_by(
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


@bp.route('/delete/cat', methods=['POST'])
@login_required
def delete_cat():
    if request.method == 'POST':
        payload = request.json
        check_data = EmployeeCategory.query.filter_by(id=payload['id'])
        if check_data.first():
            if(len(check_data.first().emp_category) != 0):
                return jsonify({'message': 'Cannot delete , data being used. '})
            else:
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

from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_required
from app.employee import bp
from app.employee.model import Employee
from app.master.model import Location, Post, Company, Department, Benefit , Appointment
from app import db
from werkzeug import secure_filename
import json
import os
from sqlalchemy.exc import IntegrityError
import shutil


ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = os.path.abspath('./app/static/uploads')
print(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@bp.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('employees/entry.html')


@bp.route('/check', methods=['GET'])
@login_required
def check():
    table_obj_members = Employee.__table__.columns
    print(table_obj_members)
    return 'HAHA'


@bp.route('/new/add', methods=['POST'])
@login_required
def add_emp():
    if request.method == 'POST':
        payload = json.loads(request.form['data'])
        emp_fields = ('name', 'dob',
                      'spousename',
                      'fathername',
                      'education',
                      'contact',
                      'curr_address',
                      'curr_city',
                      'perm_address',
                      'perm_city',
                      'pan',
                      'aadhar',
                      'reference',
                      'dateofapp',
                      'appointment',
                      'post',
                      'department',
                      'company',
                      'benefits',
                      'dateeff',
                      'salary_structure',
                      'basicpay',
                      'pf',
                      'esi',
                      'advance',
                      'advancevalue',
                      'advancenum',
                      'paidleave',
                      'incrementpr'
                      )

        # init for Employee data
        new_data = Employee()

        # TEMP folder name for employee
        tempfolder = str(payload['name']+'-' +
                         payload['dob']+'-'+payload['fathername'])

        try:
            # Adding data to table
            for fields in emp_fields:

                # Gets the str type of field from employee.name -> str(name)
                temp = str(fields)
                # print(temp)
                # if(temp in emp_fields):
                val = payload[str(temp)]
                if val is not None:

                    if temp == 'pan' and val is not None:

                        if hasattr(request.files, 'panfile'):
                            if val is "":
                                try:
                                    file = request.files['panfile']
                                    if file and allowed_file(file.filename):
                                        filename = secure_filename(
                                            file.filename)
                                        foldertemp = os.path.join(
                                            UPLOAD_FOLDER, tempfolder, 'pan')

                                        if not os.path.exists(foldertemp):
                                            os.makedirs(foldertemp)
                                        else:
                                            shutil.rmtree(foldertemp)
                                            os.makedirs(foldertemp)

                                            filetemp = os.path.join(
                                                foldertemp, filename)
                                            file.save(filetemp)
                                            setattr(
                                                new_data, 'panfile', filetemp)
                                            setattr(
                                                new_data, 'pan', val)
                                            continue
                                    else:
                                        return jsonify({'message': 'Please check filetype of Pan Card.'})
                                except KeyError:
                                    return jsonify({'message': 'Please upload <b>Pancard</b>.'})

                            else:
                                return jsonify({'message': 'Please enter <b>Pan Card Number</b>.'})

                    if temp == 'aadhar' and (val is not None):
                        if hasattr(request.files, 'panfile'):
                            if val is "":
                                try:
                                    file = request.files['aadharfile']
                                    if file and allowed_file(file.filename):
                                        filename = secure_filename(
                                            file.filename)
                                        foldertemp = os.path.join(
                                            UPLOAD_FOLDER, tempfolder, 'aadhar')

                                        if not os.path.exists(foldertemp):
                                            os.makedirs(foldertemp)
                                        else:
                                            shutil.rmtree(foldertemp)
                                            os.makedirs(foldertemp)

                                            filetemp = os.path.join(
                                                foldertemp, filename)
                                            file.save(filetemp)
                                            setattr(
                                                new_data, 'aadharfile', filetemp)
                                            setattr(
                                                new_data, 'aadhar', val)
                                            continue
                                    else:
                                        return jsonify({'message': 'Please check filetype of Aadhar Card.'})

                                except KeyError:
                                    return jsonify({'message': 'Please upload <b>Aadhar card</b>.'})
                            else:
                                return jsonify({'message': 'Please enter <b>Aadhar Card Number</b>.'})

                    if temp == 'post' and (val is not None):
                        print('inside post')
                        if val is not '-1':
                            data = Post.query.filter_by(id=int(val)).first()
                            print(data)
                            new_data.post.append(data)
                            continue
                        else:
                            return jsonify({'message': 'Please select post.'})

                    if temp == 'department' and (val is not None):
                        if val is not '-1':
                            data = Department.query.filter_by(
                                id=int(val)).first()
                            new_data.department.append(data)
                            continue
                        else:
                            return jsonify({'message': 'Please select current city.'})

                    if temp == 'company' and (val is not None):
                        if val is not '-1':
                            data = Company.query.filter_by(id=int(val)).first()
                            new_data.company.append(data)
                            continue
                        else:
                            return jsonify({'message': 'Please select company.'})
                    if temp == 'appointment' and (val is not None):
                        if val is not '-1':
                            data = Appointment.query.filter_by(id=int(val)).first()
                            new_data.appontment.append(data)
                            continue
                        else:
                            return jsonify({'message': 'Please select appointment.'})

                    if temp == 'curr_city' and (val is not None):
                        print(val)
                        if payload['curr_address'] is not None:

                            if val is not -1:
                                data = Location.query.filter_by(
                                    id=int(val)).first()
                                new_data.curr_city.append(data)
                                continue
                            else:
                                return jsonify({'message': 'Please select current city.'})
                        else:
                            continue

                    if temp == 'perm_city' and (val is not None):
                        print(val)
                        if payload['perm_address'] is not None:
                            if val is not -1:

                                data = Location.query.filter_by(
                                    id=int(val)).first()
                                new_data.perm_city.append(data)
                                continue
                            else:
                                return jsonify({'message': 'Please select permanent city.'})
                        else:
                            continue

                    if temp == 'benefits' and (len(val) is not 0):
                        for item in val:
                            data = Benefit.query.filter_by(
                                id=item['id']).first()
                            new_data.benefits.append(data)
                        continue

                    if val is not '' and temp != 'benefits':
                        print(temp, val)
                        setattr(new_data, str(temp), val)

                # else:
                #     pass

            # Code to add extra files with no name , just keys in request.files()
            # Extra ID

            try:
                file = request.files['extraidfile']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    foldertemp = os.path.join(
                        UPLOAD_FOLDER, tempfolder, 'extraid')

                    if not os.path.exists(foldertemp):
                        os.makedirs(foldertemp)
                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'extraidfile', filetemp)
                    else:
                        shutil.rmtree(foldertemp)
                        os.makedirs(foldertemp)

                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'extraidfile', filetemp)
                else:
                    return jsonify({'message': 'Please check filetype of Extra ID.'})

            except KeyError:
                pass

            except Exception as e:
                print(str(e))
                pass

            # Edu Cert ID

            try:
                file = request.files['educertfile']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    foldertemp = os.path.join(
                        UPLOAD_FOLDER, tempfolder, 'educert')

                    if not os.path.exists(foldertemp):
                        os.makedirs(foldertemp)
                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'educertfile', filetemp)
                    else:
                        shutil.rmtree(foldertemp)
                        os.makedirs(foldertemp)

                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'educertfile', filetemp)
                else:
                    return jsonify({'message': 'Please check filetype of Edu Cert.'})

            except KeyError:
                pass

            except Exception as e:
                print(str(e))
                pass

            # Resume ID

            try:
                file = request.files['resumefile']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    foldertemp = os.path.join(
                        UPLOAD_FOLDER, tempfolder, 'resume')

                    if not os.path.exists(foldertemp):
                        os.makedirs(foldertemp)
                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'educertfile', filetemp)
                    else:
                        shutil.rmtree(foldertemp)
                        os.makedirs(foldertemp)

                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'resumefile', filetemp)
                else:
                    return jsonify({'message': 'Please check filetype of Resume.'})

            except KeyError:
                pass

            except Exception as e:
                print(str(e))
                pass

            db.session.add(new_data)
            db.session.commit()
            return jsonify({'success': 'Employee added'})

        except IntegrityError as e:
            db.session.rollback()
            errorInfo = e.orig.args

            return jsonify({'message': ''+str(errorInfo[1])})

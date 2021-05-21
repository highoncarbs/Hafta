from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify

from app.employee import bp
from app.employee.model import Employee, EmployeeSchema
from app.master.model import Location, Post, Company, Department, Benefit, Appointment , City
from app import db
from werkzeug.utils import secure_filename
import json
import os
from sqlalchemy.exc import IntegrityError
import shutil

from datetime import datetime , timedelta

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif',"PDF", "PNG", "JPG", "JPEG", "GIF"])
UPLOAD_FOLDER = os.path.abspath('./app/static/uploads')

hours_added = timedelta(hours= 6) 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@bp.route('/new', methods=['GET'])
def new():
    return render_template('employees/entry.html')


@bp.route('/edit/view/<id>', methods=['GET', 'POST'])

def edit_view_employee(id):
    return render_template('employees/edit.html')


@bp.route('/update', methods=['POST'])

def update_employee():
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
                      'incrementpr',
                      'bankname',
                      'accnumber',
                      'ifsccode'
                      )

        # init for Employee data
        new_data = Employee.query.filter_by(id=payload['emp_id']).first()
        print(new_data)
       # TEMP folder name for employee
        tempfolder = str(payload['name']+'-' +
                         payload['dob']+'-'+payload['fathername'])

        try:
            # Adding data to table
            for fields in emp_fields:
                print('---', fields)
                # Gets the str type of field from employee.name -> str(name)
                temp = str(fields)
            
                val = payload[str(temp)]
                if temp == 'dob' :
                    print('#1')
                    dob = payload['dob'].replace('"' , '') 
                    dob_obj = datetime.strptime(dob , '%Y-%m-%dT%H:%M:%S.%fZ') + hours_added
                    dob_date = dob_obj.date()
                    print('#3')
                    new_data.dob = dob_date
                    print('#2')
                if temp == 'dateeff' :
                    deff = payload['dateeff'].replace('"' , '') 
                    deff_obj = datetime.strptime(deff , '%Y-%m-%dT%H:%M:%S.%fZ') + hours_added
                    deff_date = deff_obj.date()
                    new_data.dateeff = deff_date
                if temp == 'dateofapp' :
                    if val is not '' and val is not None:

                        dapp = payload['dateofapp'].replace('"' , '') 
                        dapp_obj = datetime.strptime(dapp , '%Y-%m-%dT%H:%M:%S.%fZ') + hours_added
                        dapp_date = dapp_obj.date()
                        new_data.dateofapp = dapp_date
                if val != None:

                    if temp == 'post' and (val != None):

                        if val != '-1':
                            data = Post.query.filter_by(id=int(val)).first()
                            new_data.post = []
                            new_data.post.append(data)
                            continue
                        else:
                            return jsonify({'message': 'Please select post.'})

                    if temp == 'department' and (val != None):
                        if val != '-1':
                            data = Department.query.filter_by(
                                id=int(val)).first()
                            new_data.department = []
                            new_data.department.append(data)
                            continue
                        else:
                            return jsonify({'message': 'Please select current city.'})

                    if temp == 'company' and (val != None):
                        if val != '-1':
                            data = Company.query.filter_by(id=int(val)).first()

                            new_data.company = []
                            new_data.company.append(data)
                            continue
                        else:
                            return jsonify({'message': 'Please select company.'})
                    if temp == 'appointment' and (val != None):
                        if val != '-1':
                            data = Appointment.query.filter_by(
                                id=int(val)).first()
                            new_data.appointment = []
                            new_data.appointment.append(data)
                            continue
                        else:
                            return jsonify({'message': 'Please select appointment.'})

                    if temp == 'curr_city' and (val != None):
                        if payload['curr_address'] != None:

                            if val != -1:
                                data = City.query.filter_by(
                                    id=int(val)).first()
                                new_data.curr_city = []
                                new_data.curr_city.append(data)
                                continue
                            else:
                                return jsonify({'message': 'Please select current city.'})
                        else:
                            continue

                if temp == 'perm_city' and (val != None):
                        if payload['perm_address'] != None:
                            if val != -1:

                                data = City.query.filter_by(
                                    id=int(val)).first()
                                new_data.perm_city = []
                                new_data.perm_city.append(data)
                                continue
                            else:
                                return jsonify({'message': 'Please select permanent city.'})
                        else:
                            continue

                if temp == 'benefits' and (len(val) != 0):
                    new_data.benefits = []

                    for item in val:
                        data = Benefit.query.filter_by(
                            id=item['id']).first()
                        new_data.benefits.append(data)
                    continue

                if val != '' and val != None and temp != 'benefits'  and temp != 'dob' and temp != 'dateeff' and temp != 'dateofapp' :
                    setattr(new_data, str(temp), val)

                # else:
                #     pass

            # Code for Key in request.files
            # PAN
            try:
                file = request.files['panfile']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    foldertemp = os.path.join(
                        UPLOAD_FOLDER, tempfolder, 'pan')

                    if not os.path.exists(foldertemp):
                        os.makedirs(foldertemp)
                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'panfile', filetemp)
                    else:
                        shutil.rmtree(foldertemp)
                        os.makedirs(foldertemp)

                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'panfile', filetemp)
                else:
                    return jsonify({'message': 'Please check filetype of PAN.'})

            except KeyError:
                pass

            except Exception as e:
                print(str(e))
            # AADHAR
            try:
                file = request.files['aadharfile']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    foldertemp = os.path.join(
                        UPLOAD_FOLDER, tempfolder, 'aadhar')

                    if not os.path.exists(foldertemp):
                        os.makedirs(foldertemp)
                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'aadharfile', filetemp)
                    else:
                        shutil.rmtree(foldertemp)
                        os.makedirs(foldertemp)

                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'aadharfile', filetemp)
                else:
                    return jsonify({'message': 'Please check filetype of Aadhar.'})

            except KeyError:
                pass

            except Exception as e:
                print(str(e))
                
                pass
            # Photo
            try:
                file = request.files['photofile']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    foldertemp = os.path.join(
                        UPLOAD_FOLDER, tempfolder, 'photo')

                    if not os.path.exists(foldertemp):
                        os.makedirs(foldertemp)
                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'photofile', filetemp)
                    else:
                        shutil.rmtree(foldertemp)
                        os.makedirs(foldertemp)

                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'photofile', filetemp)
                else:
                    return jsonify({'message': 'Please check filetype of Photo.'})

            except KeyError:
                pass

            except Exception as e:
                print(str(e))
                
                pass

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

            # db.session.add(new_data)
            db.session.commit()
            print('HMHMHMH')
            return jsonify({'success': 'Employee updated'})

        except IntegrityError as e:
            db.session.rollback()

            return jsonify({'message': ''+str(e)})
        except Exception as e:
            db.session.rollback()
            # errorInfo = e.orig.args

            return jsonify({'message': ''+str(e)})


@bp.route('/edit/<id>', methods=['GET', 'POST'])

def edit_employee(id):
    data = Employee.query.filter_by(id=int(id)).first()
    data_schema = EmployeeSchema()
    json_data = data_schema.dump(data)
    return jsonify(json_data)
    # return render_template('employees/edit.html')


@bp.route('/new/add', methods=['POST'])
def add_emp():
    # Needs reformating , and handling of Filename with vals

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
                      'incrementpr',
                      'bankname',
                      'accnumber',
                      'ifsccode'
                      )

        # init for Employee data
        new_data = Employee()

        # TEMP folder name for employee
        tempfolder = str(payload['name']+'-'+payload['fathername'])

        try:
            # Adding data to table
            for fields in emp_fields:

                # Gets the str type of field from employee.name -> str(name)
                temp = str(fields)
               
                val = payload[str(temp)]
                if temp == 'dob' :
                    dob = payload['dob'].replace('"' , '') 
                    dob_obj = datetime.strptime(dob , '%Y-%m-%dT%H:%M:%S.%fZ') + hours_added
                    dob_date = dob_obj.date()
                    new_data.dob = dob_date
                if temp == 'dateeff' :
                    deff = payload['dateeff'].replace('"' , '') 
                    deff_obj = datetime.strptime(deff , '%Y-%m-%dT%H:%M:%S.%fZ') + hours_added
                    deff_date = deff_obj.date()
                    new_data.dateeff = deff_date
                if temp == 'dateofapp' :
                    if val is not '' and val is not None:
                        dapp = payload['dateofapp'].replace('"' , '') 
                        dapp_obj = datetime.strptime(dapp , '%Y-%m-%dT%H:%M:%S.%fZ') + hours_added
                        dapp_date = dapp_obj.date()
                        new_data.dateofapp = dapp_date
                if val != None:


                    if temp == 'post' and (val != None):
                       
                        if val != '-1':
                            data = Post.query.filter_by(id=int(val)).first()
                            new_data.post.append(data)
                            continue
                        else:
                            return jsonify({'message': 'Please select post.'})

                    if temp == 'department' and (val != None):
                        if val != '-1':
                            data = Department.query.filter_by(
                                id=int(val)).first()
                            new_data.department.append(data)
                            continue
                        else:
                            return jsonify({'message': 'Please select current city.'})

                    if temp == 'company' and (val != None):
                        if val != '-1':
                            data = Company.query.filter_by(id=int(val)).first()
                            new_data.company.append(data)
                            continue
                        else:
                            return jsonify({'message': 'Please select company.'})
                    if temp == 'appointment' and (val != None):
                        if val != '-1':
                            data = Appointment.query.filter_by(
                                id=int(val)).first()
                            new_data.appointment.append(data)
                            continue
                        else:
                            return jsonify({'message': 'Please select appointment.'})

                    if temp == 'curr_city' and (val != None):
                        if payload['curr_address'] != None:

                            if val != -1:
                                data = City.query.filter_by(
                                    id=int(val)).first()
                                new_data.curr_city.append(data)
                                continue
                            else:
                                return jsonify({'message': 'Please select current city.'})
                        else:
                            continue

                    if temp == 'perm_city' and (val != None):
                        if payload['perm_address'] != None:
                            if val != -1:

                                data = City.query.filter_by(
                                    id=int(val)).first()
                                new_data.perm_city.append(data)
                                continue
                            else:
                                return jsonify({'message': 'Please select permanent city.'})
                        else:
                            continue

                    if temp == 'benefits' and (len(val) != 0):
                        for item in val:
                            data = Benefit.query.filter_by(
                                id=item['id']).first()
                            new_data.benefits.append(data)
                        continue

                    if val != '' and val != None and temp != 'benefits' and temp != 'dob' and temp != 'dateeff' and temp != 'dateofapp':
                        setattr(new_data, str(temp), val)

                

            # Code for Key in request.files
            # PAN
            try:
                file = request.files['panfile']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    foldertemp = os.path.join(
                        UPLOAD_FOLDER, tempfolder, 'pan')

                    if not os.path.exists(foldertemp):
                        os.makedirs(foldertemp)
                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'panfile', filetemp)
                    else:
                        shutil.rmtree(foldertemp)
                        os.makedirs(foldertemp)

                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'panfile', filetemp)
                else:
                    return jsonify({'message': 'Please check filetype of PAN.'})

            except KeyError:
                pass

            except Exception as e:
                print(str(e))
                pass
            # AADHAR
            try:
                file = request.files['aadharfile']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    foldertemp = os.path.join(
                        UPLOAD_FOLDER, tempfolder, 'aadhar')

                    if not os.path.exists(foldertemp):
                        os.makedirs(foldertemp)
                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'aadharfile', filetemp)
                    else:
                        shutil.rmtree(foldertemp)
                        os.makedirs(foldertemp)

                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'aadharfile', filetemp)
                else:
                    return jsonify({'message': 'Please check filetype of Aadhar.'})

            except KeyError:
                pass

            except Exception as e:
                print(str(e))
                pass
            # Photo
            try:
                file = request.files['photofile']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    foldertemp = os.path.join(
                        UPLOAD_FOLDER, tempfolder, 'photo')
                    print('--#1-',foldertemp)
                    print('--#2-',filename)
                    if not os.path.exists(foldertemp):
                        print('--#3-IN--',filename)
                        os.makedirs(foldertemp)
                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        setattr(new_data, 'photofile', filetemp)
                    else:
                        print('--#3-els--',filename)
                        shutil.rmtree(foldertemp)
                        os.makedirs(foldertemp)

                        filetemp = os.path.join(foldertemp, filename)
                        file.save(filetemp)
                        print('--#4-IN--',filetemp)
                        setattr(new_data, 'photofile', filetemp)
                        print('--#55-IN--',new_data.photofile)
                else:
                    return jsonify({'message': 'Please check filetype of Photo.'})

            except KeyError:
                pass

            except Exception as e:
                print(str(e))
                pass

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
        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify({'message': ''+str(e)})

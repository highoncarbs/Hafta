from app import db
from app import ma
from datetime import datetime
from app.master.model import Post, Department, Company, CompanySchema,\
    Benefit, Location, LocationSchema, PostSchema, DepartmentSchema, BenefitSchema , Appointment , AppointmentSchema , City ,CitySchema
        
from marshmallow_sqlalchemy import field_for


class TimestampMixin(object):
    created = db.Column(
        db.DateTime,  default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Employee(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    spousename = db.Column(db.String(250), default=None)
    fathername = db.Column(db.String(250), nullable=False)
    education = db.Column(db.String(250), default=None)
    contact = db.Column(db.String(250), default=None)
    curr_address = db.Column(db.String(400), default=None)
    curr_city = db.relationship('City', secondary='emp_curr_city',
                                backref='emp_curr_city', cascade='all ,delete', lazy='joined')
    perm_address = db.Column(db.String(400))
    perm_city = db.relationship('City', secondary='emp_perm_city',
                                backref='emp_perm_city', cascade='all ,delete', lazy='joined')
    pan = db.Column(db.String(250), unique=True, default=None)
    panfile = db.Column(db.String(250), default=None)
    aadhar = db.Column(db.String(250), unique=True, default=None)
    aadharfile = db.Column(db.String(250), default=None)
    photofile = db.Column(db.String(250), default=None)
    extraidfile = db.Column(db.String(250), default=None)
    educertfile = db.Column(db.String(250), default=None)
    resumefile = db.Column(db.String(250), default=None)
    reference = db.Column(db.String(250), default=None)
    dateofapp = db.Column(db.DateTime, default=None)
    appointment = db.relationship('Appointment', secondary='emp_appt',
                           backref='emp_appt', cascade='all ,delete', lazy='joined')
    post = db.relationship('Post', secondary='emp_post',
                           backref='emp_post', cascade='all ,delete', lazy='joined')
    department = db.relationship('Department', secondary='emp_department',
                                 backref='emp_department', cascade='all ,delete', lazy='joined')
    company = db.relationship('Company', secondary='emp_company',
                              backref='emp_company', cascade='all ,delete', lazy='joined')
    benefits = db.relationship('Benefit', secondary='emp_benefit',
                               backref='emp_benefit', cascade='all ,delete', lazy='joined')

    dateeff = db.Column(db.DateTime, default=None)
    salary_structure = db.Column(db.String(250), default=None)
    basicpay = db.Column(db.String(250), default=None)
    pf = db.Column(db.String(50), default=None)
    esi = db.Column(db.String(50), default=None)
    bankname = db.Column(db.String(100), default=None)
    accnumber = db.Column(db.String(50), default=None)
    ifsccode = db.Column(db.String(50), default=None)
    advance = db.Column(db.String(50), default="not")
    advancevalue = db.Column(db.Float, default=None)
    advancenum = db.Column(db.Integer, default=None)
    paidleave = db.Column(db.Integer, default=None)
    incrementpr = db.Column(db.Integer, default=None)
    flag = db.Column(db.Integer , default = 0 , nullable = False)
    __table_args__ = (db.UniqueConstraint(
        'name', 'dob', 'fathername','flag', name='emp_id'), )


db.Table('emp_curr_city',
         db.Column('emp_id', db.Integer, db.ForeignKey(
             'employee.id', ondelete='SET NULL')),
         db.Column('city_id', db.Integer, db.ForeignKey(
             'city.id', ondelete='SET NULL'))
         )

db.Table('emp_perm_city',
         db.Column('emp_id', db.Integer, db.ForeignKey(
             'employee.id', ondelete='SET NULL')),
         db.Column('city_id', db.Integer, db.ForeignKey(
             'city.id', ondelete='SET NULL'))
         )


db.Table('emp_post',
         db.Column('emp_id', db.Integer, db.ForeignKey(
             'employee.id', ondelete='SET NULL')),
         db.Column('post_id', db.Integer, db.ForeignKey(
             'post.id', ondelete='SET NULL'))
         )
db.Table('emp_appt',
         db.Column('emp_id', db.Integer, db.ForeignKey(
             'employee.id', ondelete='SET NULL')),
         db.Column('appt_id', db.Integer, db.ForeignKey(
             'appointment.id', ondelete='SET NULL'))
         )

db.Table('emp_department',
         db.Column('emp_id', db.Integer, db.ForeignKey(
             'employee.id', ondelete='SET NULL')),
         db.Column('department_id', db.Integer, db.ForeignKey(
             'department.id', ondelete='SET NULL'))
         )

db.Table('emp_company',
         db.Column('emp_id', db.Integer, db.ForeignKey(
             'employee.id', ondelete='SET NULL')),
         db.Column('company_id', db.Integer, db.ForeignKey(
             'company.id', ondelete='SET NULL'))
         )
db.Table('emp_benefit',
         db.Column('emp_id', db.Integer, db.ForeignKey(
             'employee.id', ondelete='SET NULL')),
         db.Column('benefit_id', db.Integer, db.ForeignKey(
             'benefit.id', ondelete='SET NULL'))
         )


class EmployeeBasicSchema(ma.SQLAlchemySchema ):
    id = field_for(Employee, 'id', dump_only=True)
    name = field_for(Employee, 'name', dump_only=True)
    company = ma.Nested(CompanySchema, many=True)
    basicpay = field_for(Employee, 'basicpay', dump_only=True)

    class meta:
        model = Employee


class EmployeeSchema(ma.SQLAlchemySchema ):
    id = field_for(Employee, 'id', dump_only=True)
    name = field_for(Employee, 'name', dump_only=True)
    dob = field_for(Employee, 'dob', dump_only=True)
    spousename = field_for(Employee, 'spousename', dump_only=True)
    fathername = field_for(Employee, 'fathername', dump_only=True)
    education = field_for(Employee, 'education', dump_only=True)
    contact = field_for(Employee, 'contact', dump_only=True)
    curr_address = field_for(Employee, 'curr_address', dump_only=True)
    curr_city = ma.Nested(CitySchema, many=True)

    perm_address = field_for(Employee, 'perm_address', dump_only=True)
    perm_city = ma.Nested(CitySchema, many=True)
    pan = field_for(Employee, 'pan', dump_only=True)
    panfile = field_for(Employee, 'panfile', dump_only=True)
    aadhar = field_for(Employee, 'aadhar', dump_only=True)
    aadharfile = field_for(Employee, 'aadharfile', dump_only=True)
    photofile = field_for(Employee, 'photofile', dump_only=True)
    extraidfile = field_for(Employee, 'extraidfile', dump_only=True)
    educertfile = field_for(Employee, 'educertfile', dump_only=True)
    resumefile = field_for(Employee, 'resumefile', dump_only=True)
    reference = field_for(Employee, 'reference', dump_only=True)
    dateofapp = field_for(Employee, 'dob', dump_only=True)
    post = ma.Nested(PostSchema, many=True)
    department = ma.Nested(DepartmentSchema, many=True)
    company = ma.Nested(CompanySchema, many=True)
    appointment = ma.Nested(AppointmentSchema, many=True)
    benefits = ma.Nested(BenefitSchema, many=True)
    dateeff = field_for(Employee, 'dateeff', dump_only=True)
    salary_structure = field_for(Employee, 'salary_structure', dump_only=True)
    basicpay = field_for(Employee, 'basicpay', dump_only=True)
    pf = field_for(Employee, 'pf', dump_only=True)
    esi = field_for(Employee, 'esi', dump_only=True)
    advance = field_for(Employee, 'advance', dump_only=True)
    advancevalue = field_for(Employee, 'advancevalue', dump_only=True)
    advancenum = field_for(Employee, 'advancenum', dump_only=True)
    paidleave = field_for(Employee, 'paidleave', dump_only=True)
    incrementpr = field_for(Employee, 'incrementpr', dump_only=True)

    class meta:
        model = Employee


class EmployeeMainSchema(ma.SQLAlchemySchema ):
    id = field_for(Employee, 'id', dump_only=True)
    name = field_for(Employee, 'name', dump_only=True)

    basicpay = field_for(Employee, 'basicpay', dump_only=True)
    pf = field_for(Employee, 'pf', dump_only=True)
    esi = field_for(Employee, 'esi', dump_only=True)
    post = ma.Nested(PostSchema, many=True)
    department = ma.Nested(DepartmentSchema, many=True)
    company = ma.Nested(CompanySchema, many=True)
    appointment = ma.Nested(AppointmentSchema, many=True)

    class meta:
        model = Employee


class EmployeeAdvanceSchema(ma.SQLAlchemySchema ):
    id = field_for(Employee, 'id', dump_only=True)
    name = field_for(Employee, 'name', dump_only=True)

    basicpay = field_for(Employee, 'basicpay', dump_only=True)
    advance = field_for(Employee, 'advance', dump_only=True)
    advancevalue = field_for(Employee, 'advancevalue', dump_only=True)
    advancenum = field_for(Employee, 'advancenum', dump_only=True)
    post = ma.Nested(PostSchema, many=True)
    department = ma.Nested(DepartmentSchema, many=True)
    company = ma.Nested(CompanySchema, many=True)
    appointment = ma.Nested(AppointmentSchema, many=True)


    class meta:
        model = Employee

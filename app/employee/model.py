from app import db
from app import ma
from datetime import datetime
from app.master.model import Post, Department, Company, CompanySchema,\
     Benefit, Location, LocationSchema, PostSchema, DepartmentSchema, BenefitSchema
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
    curr_city = db.relationship('Location', secondary='emp_curr_location',
                                backref='emp_curr_location', cascade='all ,delete', lazy='joined')
    perm_address = db.Column(db.String(400))
    perm_city = db.relationship('Location', secondary='emp_perm_location',
                                backref='emp_perm_location', cascade='all ,delete', lazy='joined')
    pan = db.Column(db.String(250), unique=True, default=None)
    panfile = db.Column(db.String(250), default=None)
    aadhar = db.Column(db.String(250), unique=True, default=None)
    aadharfile = db.Column(db.String(250), default=None)
    extraidfile = db.Column(db.String(250), default=None)
    educertfile = db.Column(db.String(250), default=None)
    resumefile = db.Column(db.String(250), default=None)
    reference = db.Column(db.String(250), default=None)
    dateofapp = db.Column(db.DateTime, default=None)
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
    advance = db.Column(db.String(50), default=None)
    advancevalue = db.Column(db.Float, default=None)
    advancenum = db.Column(db.Integer, default=None)
    paidleave = db.Column(db.Integer, default=None)
    incrementpr = db.Column(db.Integer, default=None)
    __table_args__ = (db.UniqueConstraint(
        'name', 'dob', 'fathername', name='emp_id'), )


db.Table('emp_curr_location',
         db.Column('emp_id', db.Integer, db.ForeignKey(
             'employee.id', ondelete='SET NULL')),
         db.Column('location_id', db.Integer, db.ForeignKey(
             'location.id', ondelete='SET NULL'))
         )

db.Table('emp_perm_location',
         db.Column('emp_id', db.Integer, db.ForeignKey(
             'employee.id', ondelete='SET NULL')),
         db.Column('location_id', db.Integer, db.ForeignKey(
             'location.id', ondelete='SET NULL'))
         )


db.Table('emp_post',
         db.Column('emp_id', db.Integer, db.ForeignKey(
             'employee.id', ondelete='SET NULL')),
         db.Column('post_id', db.Integer, db.ForeignKey(
             'post.id', ondelete='SET NULL'))
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


class EmployeeBasicSchema(ma.ModelSchema):
    id = field_for(Employee, 'id', dump_only=True)
    name = field_for(Employee, 'name', dump_only=True)
    company = ma.Nested(CompanySchema, many=True)
    basicpay = field_for(Employee, 'basicpay', dump_only=True)

    class meta:
        model = Employee


class EmployeeSchema(ma.ModelSchema):
    id = field_for(Employee, 'id', dump_only=True)
    name = field_for(Employee, 'name', dump_only=True)
    dob = field_for(Employee, 'dob', dump_only=True)
    spousename = field_for(Employee, 'spousename', dump_only=True)
    fathername = field_for(Employee, 'fathername', dump_only=True)
    education = field_for(Employee, 'education', dump_only=True)
    contact = field_for(Employee, 'contact', dump_only=True)
    curr_address = field_for(Employee, 'curr_address', dump_only=True)
    # curr_city =  field_for(Employee, 'curr_city', dump_only=True)
    perm_address = field_for(Employee, 'perm_address', dump_only=True)
    # perm_city =  field_for(Employee, 'perm_city', dump_only=True)
    pan = field_for(Employee, 'pan', dump_only=True)
    panfile = field_for(Employee, 'panfile', dump_only=True)
    aadhar = field_for(Employee, 'aadhar', dump_only=True)
    aadharfile = field_for(Employee, 'aadharfile', dump_only=True)
    extraidfile = field_for(Employee, 'extraidfile', dump_only=True)
    educertfile = field_for(Employee, 'educertfile', dump_only=True)
    resumefile = field_for(Employee, 'resumefile', dump_only=True)
    reference = field_for(Employee, 'reference', dump_only=True)
    dateofapp = field_for(Employee, 'dob', dump_only=True)
    # post =  field_for(Employee, 'post', dump_only=True)
    # department = field_for(Employee, 'department', dump_only=True)
    # company =  field_for(Employee, 'company', dump_only=True)
    # benefits =  field_for(Employee, 'benefits', dump_only=True)

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

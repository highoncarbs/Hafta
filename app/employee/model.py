from app import db
from app import ma
from datetime import datetime
from app.master.model import Post, Department, Company, Benefit, Location


class TimestampMixin(object):
    created = db.Column(
        db.DateTime,  default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Employee( TimestampMixin , db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable = False)
    dob = db.Column(db.DateTime , nullable = False )
    spousename = db.Column(db.String(250) , default = None)
    fathername = db.Column(db.String(250) , nullable = False)
    education = db.Column(db.String(250) , default = None)
    contact = db.Column(db.String(250) , default = None)
    curr_address = db.Column(db.String(400) ,default = None)
    curr_city = db.relationship('Location', secondary='emp_curr_location',
                                backref='emp_curr_location', cascade='all ,delete', lazy='joined')
    perm_address = db.Column(db.String(400))
    perm_city = db.relationship('Location', secondary='emp_perm_location',
                                backref='emp_perm_location', cascade='all ,delete', lazy='joined')
    pan = db.Column(db.String(250), unique=True ,default = None)
    panfile = db.Column(db.String(250) , default = None)
    aadhar = db.Column(db.String(250), unique=True , default = None)
    aadharfile = db.Column(db.String(250) , default = None)
    extraidfile = db.Column(db.String(250) , default = None)
    educertfile = db.Column(db.String(250), default = None)
    resumefile = db.Column(db.String(250), default = None)
    reference = db.Column(db.String(250), default = None)
    dateofapp = db.Column(db.DateTime, default = None)
    post = db.relationship('Post', secondary='emp_post',
                           backref='emp_post', cascade='all ,delete', lazy='joined')
    department = db.relationship('Department', secondary='emp_department',
                                 backref='emp_department', cascade='all ,delete', lazy='joined')
    company = db.relationship('Company', secondary='emp_company',
                              backref='emp_company', cascade='all ,delete', lazy='joined')
    benefits = db.relationship('Benefit', secondary='emp_benefit',
                               backref='emp_benefit', cascade='all ,delete', lazy='joined')

    dateeff = db.Column(db.DateTime, default = None)
    salary_structure = db.Column(db.String(250), default = None)
    basicpay = db.Column(db.String(250), default = None)
    pf = db.Column(db.String(50), default = None)
    esi = db.Column(db.String(50), default = None)
    advance = db.Column(db.String(50), default = None)
    advancevalue = db.Column(db.Float, default = None)
    advancenum = db.Column(db.Integer, default = None)
    paidleave = db.Column(db.Integer, default = None)
    incrementpr = db.Column(db.Integer, default = None)
    __table_args__ = (db.UniqueConstraint('name', 'dob','fathername', name='emp_id'), )




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


# Salary Sheet
from app import db
from app import ma
from datetime import datetime
from app.master.model import Post, Department, Company, CompanySchema,\
    Benefit, Location, LocationSchema, PostSchema, DepartmentSchema, BenefitSchema
from marshmallow_sqlalchemy import field_for
from app.employee.model import Employee, EmployeeMainSchema


class TimestampMixin(object):
    created = db.Column(
        db.DateTime,  default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class SalarySheet(TimestampMixin,  db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.relationship('Company', secondary='sal_comp',
                              backref='sal_comp', cascade='all ,delete', lazy='joined')
    month = db.Column(db.DateTime, default=None, nullable=False)
    deductionsamt = db.Column(db.Float, default=0, nullable=False)
    paidamt = db.Column(db.Float, default=0, nullable=False)
    attendence = db.Column(db.String(250), default=None, nullable=False)

    def __init__(self, month, deductionsamt, paidamt, attendence):
        self.month = month
        self.deductionsamt = deductionsamt
        self.paidamt = paidamt
        self.attendence = attendence


class SalarySheetSlips(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee = db.relationship('Employee', secondary='sal_emp',
                              backref='sal_emp', cascade='all ,delete', lazy='joined')
    adv_deduction = db.Column(db.Float, default=0, nullable=False)
    date = db.Column(db.DateTime, default=None, nullable=False)
    sheet =  db.relationship('SalarySheet', secondary='sal_slip',
                              backref='sal_slip', cascade='all ,delete', lazy='joined')

    def __init__(self  , adv_deduction , date):
        self.adv_deduction = adv_deduction 
        self.date = date 



db.Table('sal_comp',
         db.Column('comp_id', db.Integer, db.ForeignKey(
             'company.id', ondelete='SET NULL')),
         db.Column('sal_id', db.Integer, db.ForeignKey(
             'salary_sheet.id', ondelete='SET NULL'))
         )
db.Table('sal_emp',
         db.Column('emp_id', db.Integer, db.ForeignKey(
             'employee.id', ondelete='SET NULL')),
         db.Column('sal_id', db.Integer, db.ForeignKey(
             'salary_sheet_slips.id', ondelete='SET NULL'))
         )
db.Table('sal_slip',
         db.Column('sal_id', db.Integer, db.ForeignKey(
             'salary_sheet.id', ondelete='SET NULL')),
         db.Column('slip_id', db.Integer, db.ForeignKey(
             'salary_sheet_slips.id', ondelete='SET NULL'))
         )



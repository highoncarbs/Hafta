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
    # __table_args__ = (db.UniqueConstraint(
    #     'employee.id', 'date', name='att_id'), )

    def __init__(self, month, deductionsamt, paidamt, attendence):
        self.month = month
        self.deductionsamt = deductionsamt
        self.paidamt = paidamt
        self.attendence = attendence


db.Table('sal_comp',
         db.Column('comp_id', db.Integer, db.ForeignKey(
             'company.id', ondelete='SET NULL')),
         db.Column('sal_id', db.Integer, db.ForeignKey(
             'salary_sheet.id', ondelete='SET NULL'))
         )


# __table_args__ = (db.UniqueConstraint(
#     'employee.id', 'date', name='att_id'), )

# Unique Constraint over Attendence -> Needs DB level uniqueness


# class AdvanceSchema(ma.ModelSchema):
#     id = field_for(Advance, 'id', dump_only=True)
#     date = field_for(Advance, 'date', dump_only=True)
#     advanceamt = field_for(Advance, 'advanceamt', dump_only=True)
#     letter = field_for(Advance, 'letter', dump_only=True)
#     security = field_for(Advance, 'security', dump_only=True)
#     cheque_no = field_for(Advance, 'cheque_no', dump_only=True)
#     deduction = field_for(Advance, 'deduction', dump_only=True)
#     deduction_period = field_for(Advance, 'deduction_period', dump_only=True)
#     employee = ma.Nested(EmployeeMainSchema, many=True)
#     company = ma.Nested(CompanySchema, many=True)
#     trans = field_for(Advance, 'trans', dump_only=True)
#     class meta:
#         model = Advance

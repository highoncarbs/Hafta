from app import db
from app import ma
from datetime import datetime
from app.master.model import Post, Department, Company, CompanySchema,\
    Benefit, Location, LocationSchema, PostSchema, DepartmentSchema, BenefitSchema
from marshmallow_sqlalchemy import field_for
from app.employee.model import Employee, EmployeeBasicSchema


class TimestampMixin(object):
    created = db.Column(
        db.DateTime,  default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Attendence(TimestampMixin,  db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee = db.relationship('Employee', secondary='att_emp',
                               backref='att_emp', cascade='all ,delete', lazy='joined')
    company = db.relationship('Company', secondary='att_comp',
                              backref='att_comp', cascade='all ,delete', lazy='joined')

    date = db.Column(db.DateTime, default=None, nullable=False)
    daysatt = db.Column(db.Float, default=None, nullable=False)
    latecomin = db.Column(db.Float, default=None, nullable=False)
    earlygoing = db.Column(db.Float, default=None, nullable=False)
    esi = db.Column(db.Float, default=None)
    pf = db.Column(db.Float, default=None)
    tds = db.Column(db.Float, default=None)
    # __table_args__ = (db.UniqueConstraint(
    #     'employee.id', 'date', name='att_id'), )


db.Table('att_emp',
         db.Column('emp_id', db.Integer, db.ForeignKey(
             'employee.id', ondelete='SET NULL')),
         db.Column('att_id', db.Integer, db.ForeignKey(
             'attendence.id', ondelete='SET NULL'))
         )

db.Table('att_comp',
         db.Column('comp_id', db.Integer, db.ForeignKey(
             'company.id', ondelete='SET NULL')),
         db.Column('att_id', db.Integer, db.ForeignKey(
             'attendence.id', ondelete='SET NULL'))
         )


# __table_args__ = (db.UniqueConstraint(
#     'employee.id', 'date', name='att_id'), )

# Unique Constraint over Attendence -> Needs DB level uniqueness


class AttendenceSchema(ma.ModelSchema):
    date = field_for(Attendence, 'date', dump_only=True)
    daysatt = field_for(Attendence, 'daysatt', dump_only=True)
    latecomin = field_for(Attendence, 'latecomin', dump_only=True)
    earlygoing = field_for(Attendence, 'earlygoing', dump_only=True)
    esi = field_for(Attendence, 'esi', dump_only=True)
    pf = field_for(Attendence, 'pf', dump_only=True)
    tds = field_for(Attendence, 'tds', dump_only=True)

    employee = ma.Nested(EmployeeBasicSchema, many=True)
    company = ma.Nested(CompanySchema, many=True)
    basicpay = field_for(Employee, 'basicpay', dump_only=True)

    class meta:
        model = Attendence

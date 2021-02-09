from app import db
from app import ma
from datetime import datetime
from marshmallow_sqlalchemy import field_for
from app.employee.model import Employee, EmployeeMainSchema


class TimestampMixin(object):
    created = db.Column(
        db.DateTime,  default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class QuickInput(TimestampMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    employee = db.relationship('Employee', secondary='qck_emp',
                               backref='qck_emp', cascade='all ,delete', lazy='joined')

    date = db.Column(db.DateTime, default=None, nullable=False)
    report = db.Column(db.String(500), default=None)
    feedback = db.Column(db.String(20) , default=None , nullable = False)

    def __init__(self , date  , report , feedback):
        self.date = date
        self.report = report 
        self.feedback = feedback

db.Table('qck_emp',
         db.Column('emp_id', db.Integer, db.ForeignKey('employee.id', ondelete='SET NULL')),
         db.Column('qck_id', db.Integer, db.ForeignKey('quick_input.id', ondelete='SET NULL'))
         )




class QuickInputSchema(ma.SQLAlchemySchema ):
    id = field_for(QuickInput , 'id' , dump_only = True)
    date = field_for(QuickInput , 'date' , dump_only = True)
    report =  field_for(QuickInput , 'report' , dump_only = True)
    feedback=  field_for(QuickInput , 'feedback' , dump_only = True)
    employee = ma.Nested(EmployeeMainSchema, many=True)

    class meta:
        model = QuickInput
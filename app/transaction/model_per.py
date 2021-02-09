from app import db
from app import ma
from datetime import datetime
from app.master.model import Performance, PerformanceSchema
from marshmallow_sqlalchemy import field_for
from app.employee.model import Employee, EmployeeMainSchema


class TimestampMixin(object):
    created = db.Column(
        db.DateTime,  default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class TransPerformance(TimestampMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    employee = db.relationship('Employee', secondary='per_emp',
                               backref='per_emp', cascade='all ,delete', lazy='joined')

    fromdate = db.Column(db.DateTime, default=None, nullable=False)
    todate = db.Column(db.DateTime, default=None, nullable=False)
    performance_items = db.relationship("PerformanceItem",
                                  cascade="all, delete",
                                  backref="transper")
    emp_id = db.Column(db.Integer)
    def __init__(self ,emp_id , fromdate , todate):
        self.fromdate = fromdate
        self.emp_id = emp_id
        self.todate = todate 

db.Table('per_emp',
         db.Column('emp_id', db.Integer, db.ForeignKey('employee.id', ondelete='SET NULL')),
         db.Column('trans_per_id', db.Integer, db.ForeignKey('trans_performance.id', ondelete='SET NULL'))
         )

class PerformanceItem(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    trans_per_id = db.Column(db.Integer,
                         db.ForeignKey('trans_performance.id', ondelete='SET NULL'))
    performance_id = db.Column(
        db.Integer, db.ForeignKey('performance.id', ondelete='SET NULL'))
    obt_score = db.Column(db.Integer, nullable=False)

    def __init__(self, performance, obt_score):
        self.performance = performance
        self.obt_score = obt_score

    performance = db.relationship(Performance, lazy="joined")




class PerformanceItemSchema(ma.SQLAlchemySchema ):
    id = field_for(PerformanceItem , 'id' , dump_only = True)
    trans_per_id = field_for(PerformanceItem , 'trans_per_id' , dump_only = True)
    performance_id = field_for(PerformanceItem , 'performance_id' , dump_only = True)
    obt_score = field_for(PerformanceItem , 'obt_score' , dump_only = True)
    performance = ma.Nested(PerformanceSchema)
    
    class meta:
        model = PerformanceItem

class TransPerformanceSchema(ma.SQLAlchemySchema ):
    id = field_for(TransPerformance , 'id' , dump_only = True)
    fromdate = field_for(TransPerformance , 'fromdate' , dump_only = True)
    todate = field_for(TransPerformance , 'todate' , dump_only = True)
    performance_items = ma.Nested(PerformanceItemSchema, many=True)
    employee = ma.Nested(EmployeeMainSchema, many=True)

    class meta:
        model = TransPerformance
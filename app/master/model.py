from app import db
from app import ma


class Company(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    location = db.relationship('Location', secondary='company_location',
                               backref='company_location', cascade='all ,delete', lazy='joined')
    location_id = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.UniqueConstraint(
        'name', 'location_id', name='CompanyLocationConstraint'), )

    def __init__(self, name , location_id):
        self.name = name
        self.location_id = location_id


class EmployeeCategory(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)

    def __init__(self, name):
        self.name = name


class Location(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)

    def __init__(self, name):
        self.name = name

    # def __repr__(self, name):
    #     self.name = name


db.Table('company_location',
         db.Column('company_id', db.Integer, db.ForeignKey(
             'company.id', ondelete='SET NULL')),
         db.Column('location_id', db.Integer, db.ForeignKey(
             'location.id', ondelete='SET NULL'))

         )


class LocationSchema(ma.SQLAlchemySchema ):
    class Meta:
        model = Location



class City(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)

    def __init__(self, name):
        self.name = name

class CitySchema(ma.SQLAlchemySchema ):
    class Meta:
        model = City



class Appointment(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)

    def __init__(self, name):
        self.name = name


class AppointmentSchema(ma.SQLAlchemySchema ):
    class Meta:
        model = Appointment


class Department(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)

    def __init__(self, name):
        self.name = name


class DepartmentSchema(ma.SQLAlchemySchema ):
    class Meta:
        model = Department


class Post(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)

    def __init__(self, name):
        self.name = name


class PostSchema(ma.SQLAlchemySchema ):
    class Meta:
        model = Post


class Benefit(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)

    def __init__(self, name):
        self.name = name


class BenefitSchema(ma.SQLAlchemySchema ):
    class Meta:
        model = Benefit


class ModeOfPay(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)

    def __init__(self, name):
        self.name = name


class PaySchema(ma.SQLAlchemySchema ):
    class Meta:
        model = ModeOfPay


class Performance(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    score = db.Column(db.Integer , nullable= False)
    weight = db.Column(db.Integer , nullable = False)

    def __init__(self, name , score , weight):
        self.name = name
        self.score= score
        self.weight= weight


class AttendenceRules(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    late_comin = db.Column(db.Float, unique=True)
    late_comin_day = db.Column(db.Float, unique=True)
    early_going = db.Column(db.Float, unique=True)
    early_going_day = db.Column(db.Float, unique=True)
    db.CheckConstraint('id =1', name='check1')

    def __init__(self, late_comin, late_comin_day, early_going, early_going_day):
        self.late_comin = late_comin
        self.early_going = early_going
        self.late_comin_day = late_comin_day
        self.early_going_day = early_going_day


class PerformanceSchema(ma.SQLAlchemySchema ):
    class Meta:
        model = Performance

class AttendenceRuleSchema(ma.SQLAlchemySchema ):
    class Meta:
        model = AttendenceRules


class EmployeeCatSchema(ma.SQLAlchemySchema ):
    class Meta:
        model = EmployeeCategory


class CompanySchema(ma.SQLAlchemySchema ):
    location = ma.Nested(LocationSchema, many=True)

    class Meta:
        model = Company

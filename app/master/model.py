from app import db
from app import ma


class Company(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    location = db.relationship('Location', secondary='company_location',
                               backref='company_location', cascade='all ,delete', lazy='joined')

    def __init__(self, name):
        self.name = name


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


class LocationSchema(ma.ModelSchema):
    class Meta:
        model = Location


class Appointment(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)

    def __init__(self, name):
        self.name = name


class AppointmentSchema(ma.ModelSchema):
    class Meta:
        model = Appointment


class Department(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)

    def __init__(self, name):
        self.name = name


class DepartmentSchema(ma.ModelSchema):
    class Meta:
        model = Department


class Post(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)

    def __init__(self, name):
        self.name = name


class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post


class Benefit(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)

    def __init__(self, name):
        self.name = name


class BenefitSchema(ma.ModelSchema):
    class Meta:
        model = Benefit


class ModeOfPay(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)

    def __init__(self, name):
        self.name = name


class PaySchema(ma.ModelSchema):
    class Meta:
        model = ModeOfPay


class Performance(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)

    def __init__(self, name):
        self.name = name


class PerformanceSchema(ma.ModelSchema):
    class Meta:
        model = Performance


class EmployeeCatSchema(ma.ModelSchema):
    class Meta:
        model = EmployeeCategory


class CompanySchema(ma.ModelSchema):
    location = ma.Nested(LocationSchema, many=True)

    class Meta:
        model = Company

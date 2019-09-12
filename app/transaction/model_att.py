from app import db
from app import ma
from datetime import datetime
from app.master.model import Post, Department, Company, CompanySchema,\
     Benefit, Location, LocationSchema, PostSchema, DepartmentSchema, BenefitSchema
from marshmallow_sqlalchemy import field_for

# class Attendence():
#     pass
from flask import Blueprint 

bp = Blueprint('employee' , __name__ , template_folder='templates/employee')

from app.employee import add_employee ,show_employee
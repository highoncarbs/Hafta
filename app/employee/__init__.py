from flask import Blueprint 

bp = Blueprint('employee' , __name__ , template_folder='templates/auth')

from app.employee import routes
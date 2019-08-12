from flask import Blueprint 

bp = Blueprint('auth' , __name__ , template_folder='templates/auth')

from app.auth import routes
from flask import Blueprint 

bp = Blueprint('main' , __name__ , template_folder='templates/base')

from app.main import routes , firms
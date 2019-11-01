from flask import Blueprint 

bp = Blueprint('master' , __name__ , template_folder='templates/master')

from app.master import routes
from app.master import appointment , department , pay , performance , post , benefits , attendence_rules , city
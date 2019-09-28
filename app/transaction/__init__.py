from flask import Blueprint 

bp = Blueprint('transaction' , __name__ , template_folder='templates/transaction')

from app.transaction import attendence , advance , salary_sheet , performance , quickinput
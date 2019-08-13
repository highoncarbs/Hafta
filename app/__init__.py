# from flask import Flask, render_template, g, redirect, jsonify, url_for, request, session
# from flask_sqlalchemy import SQLAlchemy

# from flask_login import LoginManager, login_user, login_required, logout_user, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
# import logging
# import json
# from flask_migrate import Migrate
# # from flask_marshmallow import Marshmallow

# app = Flask(__name__)
# app.config.from_pyfile('config.py')

# db = SQLAlchemy(app)
# # ma = Marshmallow(app)

# migrate = Migrate(app, db)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# @app.route('/login', methods=['GET', 'POST'])
# def login():

#     form = LoginForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(username=form.username.data).first()
#         if user:
#             if check_password_hash(user.password, form.password.data):
                
#                 if user.roles[0].name == 'ADMIN' :
#                     login_user(user)
#                     session['mssg'] = "Hey ! " + \
#                         str(current_user.username) + " . Welcome."

#                     return redirect(url_for('home'))    
                
#                 elif user.roles[0].name == 'USER':
#                     login_user(user)
#                     session['mssg'] = "Hey ! " + \
#                         str(current_user.username) + " . Welcome."

#                     return redirect(url_for('user_home'))
#             else:
#                 session['mssg'] = "Invalid Username or Password"
#                 return render_template('login.html', subtitle="Login", form=form, mssg=session['mssg'])
#         else:
#             session['mssg'] = "Invalid Username or Password"
#             return render_template('login.html', subtitle="Login", form=form, mssg=session['mssg'])
#     if not hasattr(session, "mssg"):
#         session['mssg'] = ""
#     return render_template('login.html', subtitle="Login", form=form, mssg=session['mssg']), 200


# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = SignupForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(username=form.username.data).first()
#         if user is None:
#             hashed_pass = generate_password_hash(
#                 form.password.data, method='sha256')
#             new_user = Users(username=form.username.data,
#                              email=form.email.data, password=hashed_pass)
#             # user_table = UserTableCreator(form.email.data)
#             # Base.metadata.create_all(engine)
#             db.session.add(new_user)
#             db.session.commit()
#             db.session.close()
#             session['mssg'] = "You're all set. Please Login. "

#             return redirect(url_for('login'))
#         else:
#             session['mssg'] = "Email ID already in use. Please login"

#             return render_template('register.html', form=form, subtitle="Signup", mssg=session['mssg'])

#     return render_template('register.html', subtitle="Signup", form=form, mssg=session['mssg']), 200

import logging 
import os 
from flask import Flask , request ,current_app 
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from flask_login import LoginManager 
from flask_moment import Moment 
from config import Config 
from werkzeug.debug import DebuggedApplication

db = SQLAlchemy()
migrate = Migrate()

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'

moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app , db)
    login.init_app(app)
    moment.init_app(app)
    with app.app_context():
        db.create_all()
        
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')
    
    
    return app

from app import model

import logging
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_moment import Moment
from config import Config
from flask_cors import CORS
from werkzeug.debug import DebuggedApplication
from flask_marshmallow import Marshmallow
# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()

jwt = JWTManager()

# moment = Moment()
from datetime import timedelta

hours_added = timedelta(hours=6)
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    cors.init_app(app)

    # sentry_sdk.init(
    #     dsn="https://3313de1a38b04d3ea4ec37ea3f7ad81b@sentry.io/1759344",
    #     integrations=[FlaskIntegration()]
    # )
    with app.app_context():
        from app.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')

        from app.main import bp as main_bp
        app.register_blueprint(main_bp, url_prefix='/')

        from app.master import bp as master_bp
        app.register_blueprint(master_bp, url_prefix='/master')

        from app.employee import bp as emp_bp
        app.register_blueprint(emp_bp, url_prefix='/employee')

        from app.transaction import bp as trans_bp
        app.register_blueprint(trans_bp, url_prefix='/transaction')

        from app.report import bp as report_bp
        app.register_blueprint(report_bp, url_prefix='/reports')

        db.create_all()

        from app.model import Role
        if Role(name="ADMIN").query.first():
            pass
        else:

            db.session.add(Role(name='ADMIN'))
            db.session.commit()
    return app

from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user
from app.transaction import bp
# from app.transaction.model_att import Attendence
from app import db, ma


@bp.route('/attendence/' , methods=['GET'])
def show_attendence():
    return render_template('transaction/attendence.html')
from flask import Blueprint, render_template
from flask import render_template, redirect, url_for, request, session, jsonify
from app.auth import bp
from app.model import User, Role
from app import db , jwt
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token, get_raw_jwt 
# jwt_refresh_token_required


# @jwt.token_in_blacklist_loader
# def check_if_token_in_blacklist(decrypted_token):
#     jti = decrypted_token['jti']
#     return jti in blacklist
blacklist = set()


@bp.route('/login',  methods=['POST'])
def login():
    auth = request.json
    if auth:
        user = str(auth['username']).lower().strip()
        if user == 'admin':
            if(auth['password'] == '101'):
                access_token = create_access_token(identity=auth['username'])
                refresh_token = create_refresh_token(identity=auth['username'])
                return jsonify({'token': access_token, 'refresh_token': refresh_token})
            else:
                return jsonify({'message': "Invalid Data"})
        else:
            return jsonify({'message': "Invalid Data"})

    else:
        return jsonify({'message': "Invalid Data"})


# @bp.route('/refresh', methods=['POST'])
# @jwt_refresh_token_required
# def refresh():
#     current_user = get_jwt_identity()
#     ret = {
#         'token': create_access_token(identity=current_user)
#     }
#     return jsonify(ret), 200


@bp.route('/user', methods=['GET'])
@jwt_required
def get_user_details():
    try:
        current_user = get_jwt_identity()
        return jsonify({'user': {'name': current_user}})
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Unable to load user.'})


@bp.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200

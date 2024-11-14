#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv
from api.v1.app import auth


@app_views.route('auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """ POST /api/v1/auth_session/login
            - starting a session
    """
    if request.form.get("email") == "" or not request.form.get("email"):
        return jsonify({"error": "email missing"}), 400

    if request.form.get("password") == "" or not request.form.get("password"):
        return jsonify({"error": "password missing"}), 400

    dictt = {}
    dictt["email"] = request.form.get("email")

    user_exist = User.search(dictt)
    if not user_exist:
        return jsonify({"error": "no user found for this email"}), 404

    for user in user_exist:
        if not user.is_valid_password(request.form.get("password")):
            return jsonify({"error": "wrong password"}), 401
        else:
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(getenv("SESSION_NAME"), session_id)
            return response


@app_views.route('auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def auth_session_logout():
    """ DELETE /api/v1/auth_session/logout
            - delete user session
    """
    destroy_session = auth.destroy_session(request)
    if not destroy_session:
        abort(404)
    else:
        return jsonify({}), 200

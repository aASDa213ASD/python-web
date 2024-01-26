from .                  import api_accounts
from ..accounts.models  import User
from ...                import db, bcrypt, jwt_manager, jwt_blocklist
from config             import ACCESS_EXPIRES

from flask              import request, jsonify
from flask_restful      import Resource, Api
from flask_jwt_extended import (
    jwt_required, create_access_token,
    create_refresh_token, get_jwt_identity, get_jwt
)
from flask_httpauth     import HTTPBasicAuth


basic_auth = HTTPBasicAuth()


@api_accounts.route('/heartbeat', methods=['GET'])
def ping():
    return jsonify({"message" : "Beep"})

@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return username


@basic_auth.error_handler
def auth_error(status):
    return jsonify(message="Invalid input"), status


@api_accounts.route('/login', methods=['POST'])
@basic_auth.login_required
def login():
    access_token = create_access_token(identity=basic_auth.current_user())
    refresh_token = create_refresh_token(identity=basic_auth.current_user())
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@api_accounts.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(msg="Token was refreshed successfully", access_token=access_token)


@jwt_manager.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_blocklist.get(jti)
    return token_in_redis is not None


@api_accounts.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    jti = token["jti"]
    token_type = token["type"]
    jwt_blocklist.set(jti, "", ex=ACCESS_EXPIRES[token_type])

    return jsonify(msg=f"{token_type.capitalize()} token successfully revoked")
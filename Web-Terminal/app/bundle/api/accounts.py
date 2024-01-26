from .                  import api_accounts
from ..accounts.models  import User
from ...                import db, bcrypt, jwt_manager, jwt_blocklist
from .accounts_schemas   import SingleUserSchema, MultipleUserSchema, GetSingleUserSchema
from config             import ACCESS_EXPIRES

from flask              import request, jsonify, make_response
from flask_restful      import Resource, Api
from flask_jwt_extended import (
    jwt_required, create_access_token,
    create_refresh_token, get_jwt_identity, get_jwt
)
from flask_httpauth     import HTTPBasicAuth
from marshmallow        import ValidationError


basic_auth = HTTPBasicAuth()
api        = Api(api_accounts)
single_user_schema = SingleUserSchema()
multiple_users_schema = MultipleUserSchema(many=True)


class UsersApi(Resource):
    def get(self):
        users = User.query.all()
        return make_response(jsonify({'users': multiple_users_schema.dump(users)}), 200)

    def post(self):  # username, email, image_file, password
        try:
            data = request.get_json()
            user = single_user_schema.load(data)
        except ValidationError as err:
            errors = {field: messages[0] if isinstance(messages, list) else messages for field, messages in err.messages.items()}
            return make_response(jsonify(errors), 400)

        new_user = User(**user)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception:
            return make_response(jsonify({'message': 'User data has been duplicated'}), 400)

        return make_response(jsonify({'message': 'User has been created'}), 201)


class UserApi(Resource):
    get_single_user_schema = GetSingleUserSchema()
    single_user_schema = SingleUserSchema()
    multiple_users_schema = MultipleUserSchema(many=True)

    def get(self, id):
        user = User.query.get(id)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)

        user_data = self.get_single_user_schema.dump(user)
        return make_response(jsonify(user_data), 200)

    def put(self, id):
        user = User.query.get(id)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)

        try:
            data = self.single_user_schema.load(request.get_json(), partial=True)  # Enable partial loading
            if 'password' in data:
                hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
                data['password'] = hashed_password


            for key, value in data.items():
                setattr(user, key, value)

            db.session.commit()
        except ValidationError as err:
            errors = {field: messages[0] if isinstance(messages, list) else messages for field, messages in
                      err.messages.items()}
            return make_response(jsonify(errors), 400)
        except Exception:
            db.session.rollback()
            return make_response(jsonify({'message': 'Failed to update user'}), 400)

        return make_response(jsonify({'message': 'User has been updated'}), 200)

    def delete(self, id):
        user = User.query.get(id)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)

        try:
            db.session.delete(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return make_response(jsonify({'message': 'Failed to delete user'}), 400)

        return make_response(jsonify({'message': 'User has been deleted'}), 200)


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

api.add_resource(UsersApi, '/users')
api.add_resource(UserApi, '/user/<int:id>')
from marshmallow import Schema, fields as ma_fields, validate, ValidationError
from marshmallow.decorators import validates

from ..accounts.models import User


class SingleUserSchema(Schema):
    username = ma_fields.Str(required=True, validate=validate.Length(min=1, error="Username is required"))

    @validates("username")
    def validates_username(self, username):
        if User.query.filter(User.username == username).first():
            raise ValidationError("That username is taken")
        
    image_file = ma_fields.Str()
    password = ma_fields.Str(required=True, validate=validate.Length(min=6, error="That password is too small"))

    @validates("password")
    def validates_password(self, password):
        if password == '':
            raise ValidationError("Password is required")


class GetSingleUserSchema(Schema):
    username = ma_fields.Str(required=True, validate=validate.Length(min=1, error="Username is required"))

    @validates("username")
    def validates_username(self, username):
        if User.query.filter(User.username == username).first():
            raise ValidationError("That username is taken")
    
    image_file = ma_fields.Str()

    @staticmethod
    def get_user(data):
        return GetSingleUserSchema().load(data)


class MultipleUserSchema(Schema):
    username = ma_fields.Str(required=True, validate=validate.Length(min=1, error="Username is required"))
    image_file = ma_fields.Str()

    @staticmethod
    def get_users():
        users = User.query.all()
        return users

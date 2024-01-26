from secrets import token_hex
from datetime import timedelta


ACCESS_EXPIRES = {
    'access':  timedelta(minutes=30),
    'refresh': timedelta(days=1)
}


class Config:
    """ Key Sample: d34f10e61bce200546cf659cbd14d405 """
    SECRET_KEY = token_hex(16)
    JWT_SECRET_KEY = token_hex(16)
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES['access']
    JWT_REFRESH_TOKEN_EXPIRES = ACCESS_EXPIRES['refresh']
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:9754@localhost/terminal"


class Development(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False


class Testing(Config):
    TESTING          = True
    DEBUG            = True
    WTF_CSRF_ENABLED = False

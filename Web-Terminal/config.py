from secrets import token_hex


class Config:
    """ Key Sample: d34f10e61bce200546cf659cbd14d405 """
    SECRET_KEY = token_hex(16)
    JWT_SECRET_KEY = token_hex(16)
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:9754@localhost/terminal"


class Development(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False

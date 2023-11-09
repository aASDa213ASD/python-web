from secrets import token_hex

""" Sample: d34f10e61bce200546cf659cbd14d405 """
SECRET_KEY = token_hex(16)
WTF_CSRF_ENABLED = True
SQLALCHEMY_DATABASE_URI = "mariadb+pymysql://root:9754@localhost/web-terminal"

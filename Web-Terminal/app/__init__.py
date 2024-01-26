from flask              import Flask
from flask_restful      import Api
from flask_bcrypt       import Bcrypt
from flask_migrate      import Migrate
from flask_login        import LoginManager
from flask_sqlalchemy   import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
api_instance = Api()
jwt = JWTManager()
migrate = Migrate()


def create_app(config_name: str = "dev"):
    app = Flask(__name__)
    
    from config import Development, Production, Testing

    if config_name == "prod":
        app.config.from_object(Production)
    elif config_name == "test":
        app.config.from_object(Testing)
    else:
        app.config.from_object(Development)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'accounts.login'
    login_manager.login_message_category = 'info'
    api_instance.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from .bundle.main.views import main
        from .bundle.accounts.views import accounts
        from .bundle.cookies.views import cookies
        from .bundle.feedback.views import feedback
        from .bundle.todo.views import todo
        from .bundle.api.views import api
        from .bundle.posts.views import posts

        app.register_blueprint(main)
        app.register_blueprint(accounts)
        app.register_blueprint(cookies)
        app.register_blueprint(feedback)
        app.register_blueprint(todo)
        app.register_blueprint(api, url_prefix='/api')
        app.register_blueprint(posts)

    return app

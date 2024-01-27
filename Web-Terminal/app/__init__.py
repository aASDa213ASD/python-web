from flask              import Flask
from flask_restful      import Api
from flask_bcrypt       import Bcrypt
from flask_migrate      import Migrate
from flask_login        import LoginManager
from flask_sqlalchemy   import SQLAlchemy
from flask_jwt_extended import JWTManager
from redis              import StrictRedis


db            = SQLAlchemy()
migrate       = Migrate()
bcrypt        = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'accounts.login'
login_manager.login_message_category = 'info'
api_instance  = Api()
jwt_manager   = JWTManager()
jwt_blocklist = StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


def create_app(config_name: str = "prod"):
    app = Flask(__name__)
    
    from config import Development, Production, Test

    match(config_name):
        case "prod":
            app.config.from_object(Production)
        case "dev":
            app.config.from_object(Development)
        case "test":
            app.config.from_object(Test) 

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    api_instance.init_app(app)
    jwt_manager.init_app(app)

    with app.app_context():
        from .bundle.main.views     import main
        from .bundle.accounts.views import accounts
        from .bundle.cookies.views  import cookies
        from .bundle.feedback.views import feedback
        from .bundle.todo.views     import todo
        from .bundle.posts.views    import posts
        from .bundle.api.todo       import api_todo
        from .bundle.api.accounts   import api_accounts
        from .bundle.swagger        import swaggerui_blueprint

        app.register_blueprint(main)
        app.register_blueprint(accounts)
        app.register_blueprint(cookies)
        app.register_blueprint(feedback)
        app.register_blueprint(todo)
        app.register_blueprint(posts)
        app.register_blueprint(api_todo)
        app.register_blueprint(api_accounts)
        app.register_blueprint(swaggerui_blueprint, url_prefix="/swagger")

    return app

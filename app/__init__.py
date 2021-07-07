from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from config import config

bootstrap = Bootstrap()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)

    from .main import main as main_bluprint
    app.register_blueprint(main_bluprint)

    from .auth import auth as auth_bluprint
    app.register_blueprint(auth_bluprint, url_prefix='/auth')

    return app
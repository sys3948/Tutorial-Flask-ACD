from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from config import config

bootstrap = Bootstrap()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name]) # config.py에 작성된 설정들을 임포트 하기 위해서 Flask(__name__).config.from_object()를 사용하여 임포트를 한다.
    config[config_name].init_app(app) # 임포트 후 초기화를 한다.

    #  5,6 line에서 생성한 확장들을 init_app() 메소드를 통해서 초기화를 한다.
    bootstrap.init_app(app)
    mail.init_app(app)

    # 각 view func & route 기능인 /main, /auth를 blueprint를 이용하여 연결하는 부분.
    from .main import main as main_bluprint
    app.register_blueprint(main_bluprint)

    from .auth import auth as auth_bluprint
    app.register_blueprint(auth_bluprint, url_prefix='/auth')

    return app
import sys
sys.path.append('d:/uploadGit/account_info')
import google_info as g_info

class Config:
    SECRET_KEY = 'hard secret key token'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = g_info.account_h

    @staticmethod
    def init_app(app):
        # 초기화를 수행하기 위한 메소드. 초기화만 하기 위해서 빈 메소드로 처리.
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    
    MAIL_USERNAME = g_info.account_h
    MAIL_PASSWORD = g_info.password_h
    import mysql_info as m_info
    DB_USER = m_info.account_c
    DB_PASSWD = m_info.password_c


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}
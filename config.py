"""Config file."""
import os
basedir = os.path.abspath(os.path.dirname(__file__))
print("this is the current directory {}".format(__file__))

class Config(object):
    """Common configurations."""

    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """Development configurations."""

    DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/bucketlist_db'


class TestingConfig(Config):
    """Development configurations."""

    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = ("sqlite:///" +
                                os.path.join(basedir, 'testing.db'))


class ProductionConfig(Config):
    """Production configurations."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

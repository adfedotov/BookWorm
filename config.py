class Config(object):
    DEBUG = False
    SECRET_KEY = 'test'

class ProductionConfig(Config):
    ENV = 'production'
    DATABASE_URI = ''

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True

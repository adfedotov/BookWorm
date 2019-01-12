class Config(object):
    DEBUG = False
    SECRET_KEY = 'test'
    RECAPTCHA_PUBLIC_KEY = '6LcOIYkUAAAAAOmhBzWEg2GlPZtuhC9b9pzNOEJf'
    RECAPTCHA_PRIVATE_KEY = '6LcOIYkUAAAAADKKsOKsjI8KxFFo7AmzQjeZpt-E'

class ProductionConfig(Config):
    ENV = 'production'
    DATABASE_URI = ''

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True

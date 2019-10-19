class Config(object):
    DEBUG = False
    SECRET_KEY = 'secretkey'
    GOODREADS_API_KEY = 'YoutGoodReadsAPIKey'


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'YourDatabaseURI'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:test@localhost:5432/bookworm'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

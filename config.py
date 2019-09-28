class Config(object):
    DEBUG = False
    SECRET_KEY = 'secretkey'
    GOODREADS_API_KEY = 'YoutGoodReadsAPIKey'


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'YourDatabaseURI'


class DevelopmentConfig(Config):
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:test@localhost:5432/bookworm'
    DEBUG = True

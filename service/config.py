import os


class Config:
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = os.environ.get("DEV_MONGO_URI")


class TestingConfig(Config):
    TESTING = True
    MONGO_URI = os.environ.get("DEV_MONGO_URI")


class ProductionConfig(Config):
    MONGO_URI = os.environ.get("PROD_MONGO_URI")

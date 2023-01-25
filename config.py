import os


class BaseConfig:
    TESTING = False
    DEBUG = False
    TEMPLATES_FOLDER = "templates"


class DevelopmentConfig(BaseConfig):
    FLASK_ENV = "development"
    DEBUG = True


class ProductionConfig(BaseConfig):
    FLASK_ENV = "production"
    DEBUG = False


env = os.getenv("APP_ENV", "development")
if env == "development":
    config = DevelopmentConfig()
elif env == "production":
    config = ProductionConfig()

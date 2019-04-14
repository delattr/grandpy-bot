import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default')
    MAPS_API_KEY = os.environ.get('MAPS_API_KEY')
    PLACE_API_KEY = os.environ.get('PLACE_API_KEY')

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False



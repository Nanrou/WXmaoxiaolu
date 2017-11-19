from os import getenv


class DevConfig:
    TOKEN = None,
    SERVER = "auto",
    HOST = "127.0.0.1",
    PORT = "8888",
    SESSION_STORAGE = None,
    APP_ID = '1234567',
    APP_SECRET = '1234567',
    ENCODING_AES_KEY = 'lulu'


class ProdConfig:
    TOKEN = None,
    SERVER = "auto",
    HOST = "127.0.0.1",
    PORT = "8888",
    SESSION_STORAGE = getenv('SESSION_STORAGE') or None,
    APP_ID = getenv('APP_ID') or None,
    APP_SECRET = getenv('APP_SECRET') or None,
    ENCODING_AES_KEY = getenv('ENCODING_AES_KEY') or None


config_dict = {'dev': DevConfig, 'prod': ProdConfig}

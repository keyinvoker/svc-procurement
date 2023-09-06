import os
from dotenv import find_dotenv, load_dotenv
from logging.config import dictConfig

from procurement.tools.env import Env


load_dotenv(find_dotenv())

env = Env()


def _get_log_filename(log_filename: str):
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(here, os.pardir, 'procurement/logs', f'{log_filename}.log')


class Config:
    SECRET_KEY = env.string("SECRET_KEY", "top-ten-world-secret")

    DB_HOST = env.string("DB_HOST", "localhost")
    DB_PORT = env.string("DB_PORT", "5432")
    DB_NAME = env.string("DB_NAME", "procurement")
    DB_USER = env.string("DB_USER", "")
    DB_PASS = env.string("DB_PASS", "")
    DB_CONNECT_STRING = (
        f"postgresql+pg8000://{ DB_USER }:{ DB_PASS }@"
        f"{ DB_HOST }:{DB_PORT}/{ DB_NAME }"
    )
    SQLALCHEMY_DATABASE_URI = DB_CONNECT_STRING
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Logging Config
    LOGGING_CONFIG = {
        'version': 1,
        'formatters': {
            'simple': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        },
        'handlers': {
            'file_app': {
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 1000000000,
                'backupCount': 5,
                'level': 'INFO',
                'formatter': 'simple',
                'filename': _get_log_filename('app'),
            },
            'file_error': {
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 1000000000,
                'backupCount': 5,
                'level': 'ERROR',
                'formatter': 'simple',
                'filename': _get_log_filename('error'),
            },
            'console': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'simple',
            },
        },
        'loggers': {
            'app': {
                'handlers': ['console', 'file_app'],
                'propagate': False,
            },
            'error': {
                'handlers': ['console', 'file_error'],
                'propagate': False,
            },
        },
        'root': {'level': 'INFO', 'handlers': ['console', 'file_error']},
    }
    dictConfig(LOGGING_CONFIG)

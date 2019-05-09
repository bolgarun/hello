import os

USER_URI = os.environ.get('USER')
PASSWORD_URI = os.environ.get('PASSWORD')
NAME_URI = os.environ.get('NAME')


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@localhost/{}'.format(USER_URI, PASSWORD_URI, NAME_URI)
    API_KEY_SENDGRID = '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'
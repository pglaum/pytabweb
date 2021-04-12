import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        print('fatal: no secret key')
        exit(1)

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        print('fatal: no database uri')
        exit(1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CONFIGURATION_FILE = os.environ.get('CONFIGURATION_FILE') or \
        os.path.join(basedir, 'config.json')

    DATA_DIR = os.environ.get('DATA_DIR')
    if not DATA_DIR:
        print('fatal: no data dir')
    else:
        if not os.path.isdir(DATA_DIR):
            os.makedirs(DATA_DIR)

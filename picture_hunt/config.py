import os

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOADS = os.path.join(basedir, 'static/tmp')
S3_BUCKET = 'picture-hunt'

SQLALCHEMY_DATABASE_PATH = os.path.join(basedir, '../pic.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLALCHEMY_DATABASE_PATH

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

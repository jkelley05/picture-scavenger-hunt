import os
import socket
from picture_hunt.secrets import DB_USER, DB_PASSWD

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOADS = os.path.join(basedir, 'static/tmp')
S3_BUCKET = 'picture-hunt'


if socket.gethostname() == "aws":
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{passwd}@localhost/pic'.format(user=DB_USER, passwd=DB_PASSWD)
else:
    SQLALCHEMY_DATABASE_PATH = os.path.join(basedir, '../pic.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLALCHEMY_DATABASE_PATH

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

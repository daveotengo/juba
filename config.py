import os

basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Dadapapa4141@localhost:3306/juba"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = True
SECRET_KEY = 'SuperSecretKey'

# mail server settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'daveotengo@gmail.com'
MAIL_PASSWORD = 'Dadapapa41414141@'
MAIL_USE_SSL=True
MAIL_USE_TLS=False

APP_NAME = "JUBA"



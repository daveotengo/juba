

from flask_mail import Message, Mail


from flask import Flask

from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy

from flask_login import LoginManager







#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
from config import MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_USE_TLS, MAIL_USE_SSL, SECRET_KEY, \
    SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

# Open database connection
#dbhost = secrets.dbhost
#dbuser = secrets.dbuser
#dbpass = secrets.dbpass
#dbname = secrets.dbname

#db = pymysql.connect(dbhost, dbuser, dbpass, dbname)

app = Flask(__name__)
app.config.from_object('config')
app.config['MAIL_SERVER']=MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
mail = Mail(app)

login = LoginManager(app)
login.login_view = 'login'
login.login_message_category = 'danger' # sets flash category for the default message 'Please log in to access this page.'



app.config['SECRET_KEY']=SECRET_KEY
# import os
# = os.environ.get('SECRET_KEY')


# Prevent --> pymysql.err.OperationalError) (2006, "MySQL server has gone away (BrokenPipeError(32, 'Broken pipe')
class SQLAlchemy(_BaseSQLAlchemy):
     def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(app, options)
        options["pool_pre_ping"] = True
# <-- MWC


app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS #will be false silence the deprecation warning
db = SQLAlchemy(app)

#db.create_all()


from app import views, models, auth






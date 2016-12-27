from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# Update config parameters for the use of the application

# Set the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:bukmacher@localhost/betepl'

app.config['SECRET_KEY'] = 'super-secret'

# Enable registering users
app.config['SECURITY_REGISTERABLE'] = True

# Enable confirming registration by email
app.config['SECURITY_CONFIRMABLE'] = False

# Enable recovering passwords
app.config['SECURITY_RECOVERABLE'] = True

# Set passwords hash and salt
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
app.config['SECURITY_PASSWORD_SALT'] = 'fhasdgihwntlgy8f'

# Enable sending emails to users
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'bet.epl.info@gmail.com',
    MAIL_PASSWORD = 'bukmacher',
))


app.debug = True


db = SQLAlchemy(app)
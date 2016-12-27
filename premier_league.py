# Import necessary packages
from app import app, db
from flask.ext.mail import Mail

from flask_sqlalchemy import SQLAlchemy


from flask.ext.security import Security, SQLAlchemyUserDatastore


#print(sys.path)

def init_db():
	db.create_all()
	db.session.commit()
	# from models import User
	# user = User()
	# user.username = "admin"
	# user.password = 'gosia1'
	# user.email = 'gosia@pl.pl'
	# db.session.add(user)
	# db.session.commit()

# Setup mail extension
mail = Mail(app)

if __name__ == "__main__":
	from models import *
	init_db()


# Setup Flask-Security

def init_wird_stuff():
	from models import User, Role
	from forms import ExtendedRegisterForm
	user_datastore = SQLAlchemyUserDatastore(db, User, Role)
	security = Security(app, user_datastore, register_form=ExtendedRegisterForm)	
	return user_datastore, security

	
	
user_datastore, security = 	init_wird_stuff()
 


if __name__ == "__main__":
	from views import *
	app.run()

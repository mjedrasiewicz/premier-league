
from wtforms.validators import Required
from flask.ext.wtf import Form  
from wtforms.validators import DataRequired
from flask_security.forms import RegisterForm
from wtforms import (
    Form,
    validators,
    TextAreaField,
    IntegerField,
    BooleanField,
    SelectField,
    DateField,
    FloatField,
    StringField,
)
from models import User

# Exted registration form with username field
class ExtendedRegisterForm(RegisterForm):  

	# Add username field to the register's class
    username = StringField('username', [DataRequired()])

    def validate(self):
		# Add username validation: return: True is the form is valid
        
        # Use standard validator
        validation = Form.validate(self)
        if not validation:
            return False

        # Check if username already exists       
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            # Text displayed to the user
            self.username.errors.append('Username already exists')
            return False

        return True

#class AddBet(Form):

#	bet = SelectField(
#		'bet',
#		choices=[
#			(' --- ', ' --- '),
#			('hosts', 'Gospodarze'),
#			('guests', 'Goœcie'),
#			('drawn', 'Remis'),
#	]
#)
	
#	points = SelectField(
#		'points',
#		choices=[
#			(str(i), i) for i in range(11)
#	]
#)
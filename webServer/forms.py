from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField, ValidationError
from wtforms.validators import Required, Email
import datetime
import logging

def ValidateBirthday(form, field):
	if datetime.date(1910, 1, 1) > field.data:
		raise ValidationError("You're a bit too old...")
	elif datetime.now() < field.data:
		raise ValidationError("You're not born yet...")

def CheckIfValidDay(form, field):
	try:
		field.data = int(field.data)
		if field.data in range(1, 31):
			return True
		else:
			raise ValidationError("Invalid birthday.")
	except:
		logging.warning("AAAH")
		raise ValidationError("Invalid birthday.")

class registerForm(Form):
	firstName = StringField("First Name", validators=[Required()])
	lastName = StringField("Last Name", validators=[Required()])
	username = StringField("Username", validators=[Required()])
	email = StringField("Email", validators = [Required(), Email()])
	birthday_month = SelectField("Month", choices = [("jan","January"), ("feb","February"),
														("mar","March"),("apr","April"),("may","May"), 
														("jun","June"), ("jul","July"),("aug","August"),
														("sep","September"), ("oct","October"), ("nov","November"), ("dec","December")], 
								validators = [Required()])
	birthday_day = StringField("Day", validators = [Required(), CheckIfValidDay])
	_years = range(1910, datetime.date.today().year+1)
	birthday_year = SelectField("Year", choices = [(str(i), str(i)) for i in _years], validators = [Required()])
	# password
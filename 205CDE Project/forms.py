from wtforms import Form,TextField, TextAreaField,StringField, PasswordField, validators, IntegerField



class RegisterForm(Form):
	password=PasswordField('password',[validators.DataRequired(),validators.length(min=1,max=50),validators.EqualTo('confirm', message ='Password Not Match')])
	userName=StringField('userName',[validators.length(min=1,max=50)])
	email=StringField('email',[validators.length(min=6,max=50),validators.Email("please enter a correct email address" )])
	address=StringField("address")
	confirm=PasswordField("Confirmed Password")
	
class addForm(Form):
	dishName=StringField('dishName',[validators.DataRequired(),validators.length(min=1,max=100)])
	price=IntegerField('price',[validators.DataRequired()])


class orderForm(Form):
	dishName=StringField('dishName',[validators.DataRequired()])
	process_methods=TextAreaField('process_methods',[validators.DataRequired(),validators.length(min=1)])
	number=StringField('number',[validators.DataRequired(),validators.length(min=1)])

class userNameForm(Form):
	userName=StringField('userName',[validators.DataRequired()])

class emailForm(Form):
	email=StringField('email',[validators.Email('please enter a correct email address')])

class passwordForm(Form):	
	password=StringField('password',[validators.DataRequired()])

class addressForm(Form):	
	address=StringField('address',[validators.DataRequired()])
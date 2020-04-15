from flask import Flask, render_template, flash,  request, session, redirect, url_for, logging
from forms import RegisterForm ,orderForm, userNameForm,emailForm,passwordForm,addressForm,addForm
from flask_mysqldb import MySQL
from functools import wraps

app= Flask(__name__)

app.secret_key="averysecretkey"

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='205CDE'
app.config['MYSQL_PASSWORD']='12345'
app.config['MYSQL_DB']='project'
app.config['MYSQL_CURSORCLASS']='DictCursor'


mysql=MySQL(app)

def is_stafflogged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'staffName' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized access','danger')
			return redirect(url_for('login'))
	return wrap

def is_userlogged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'userName' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized access','danger')
			return redirect(url_for('login'))
	return wrap

@app.route("/")
def firstpage():
	return render_template('firstpage.html')

@app.route("/homepage")
def homepage():
		return render_template('homepage.html')

@app.route('/menu')
def menu():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM menu")
	u=cur.fetchall()
	return render_template("menu.html", u=u)
	
@app.route('/menu/order',methods=['POST','GET'])
@is_userlogged_in
def order():
	form = orderForm(request.form)
	if request.method == "POST" and form.validate():
		dishName=request.form["dishName"]
		methods=request.form["process_methods"]
		number=request.form["number"]

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO orders( dishName,process_methods,number_dish,userName) VALUES  (%s,%s,%s,%s)",(dishName,methods,number,session['userName']))
		
		mysql.connection.commit()
		flash('order ordered','success')
		return redirect(url_for('yourorder'))
		cur.close()
	return render_template('order.html',form=form)

@app.route('/menu/order/delete_order/<string:orderID>',methods=['POST','GET'])
@is_userlogged_in
def delete_order(orderID):
	cur= mysql.connection.cursor()
	
	cur.execute("DELETE FROM orders WHERE orderID = %s",[orderID])

	mysql.connection.commit()	
	flash('Deleted order','success')
	return redirect(url_for('yourorder'))
	cur.close()

@app.route('/menu/order/edit/<string:orderID>',methods=['POST','GET'])
@is_userlogged_in
def edit_order(orderID):
	cur= mysql.connection.cursor()
	form = orderForm(request.form)
	result=cur.execute("SELECT * FROM orders WHERE orderID = %s",[orderID])
	if result<0:

		order= cur.fetchone()

		form = orderForm(request.form)

		form.dishName.data= order['dishName']
		form.process_methods.data= order['process_methods']
		form.number.data= order['number_dish']


	if request.method == "POST" and form.validate():
		userName=session['userName']
		dishName=form.dishName.data
		methods=form.process_methods.data
		number=form.number.data

		cur = mysql.connection.cursor()

		cur.execute("UPDATE orders SET userName=%s,dishName=%s,number_dish=%s, process_methods=%s WHERE orderID=%s",(userName,dishName,number, methods, orderID))
		
		mysql.connection.commit()

		
		flash('Updated order','success')
		return redirect(url_for('yourorder'))
		cur.close()
	return render_template('edit_order.html',form=form)

@app.route("/yourorder")
@is_userlogged_in
def yourorder():
	userName=session['userName']

	cur = mysql.connection.cursor()
	result=cur.execute("SELECT * FROM orders WHERE userName=%s",([userName]))

	orders=cur.fetchall()

	if result > 0:
		return render_template('yourorder.html', orders=orders)
	else:
		msg="You didn't ordered any thing"
		return render_template('yourorder.html', msg=msg)
	cur.close()

@app.route('/profile')
@is_userlogged_in
def profile():
	userName=session['userName']
	cur= mysql.connection.cursor()

	cur.execute("SELECT * FROM users WHERE userName=%s",([userName]))

	users=cur.fetchall()

	return render_template('profile.html',users=users)
	
	cur.close()

	

@app.route('/profile/userName',methods=["POST","GET"])
@is_userlogged_in
def edit_userName():
	form = userNameForm(request.form)
	if request.method == "POST" and form.validate():
		userName=form.userName.data


		users=session['userName']
		session.pop('userName',None)
		session['userName']=userName
		cur= mysql.connection.cursor()

		cur = mysql.connection.cursor()

		cur.execute("UPDATE users SET userName=%s WHERE userName=%s",(userName,users))
		cur.execute('UPDATE orders SET userName=%s WHERE userName=%s',(userName,users))

		mysql.connection.commit()

		
		flash('Updated personal info','success')
		return redirect(url_for('homepage'))
		cur.close()
	return render_template('edit_userName.html',form=form)

@app.route('/profile/email',methods=["POST","GET"])
@is_userlogged_in
def edit_email():
	form = emailForm(request.form)
	if request.method == "POST" and form.validate():
		email=form.email.data
		users=session['userName']
		cur= mysql.connection.cursor()


		cur = mysql.connection.cursor()

		cur.execute("UPDATE users SET email=%s WHERE userName=%s",(email,users))

		mysql.connection.commit()
		
		flash('Updated personal info','success')
		return redirect(url_for('homepage'))
		cur.close()
	return render_template('edit_email.html',form=form)

@app.route('/profile/password',methods=["POST","GET"])
@is_userlogged_in
def edit_password():
	form = passwordForm(request.form)
	if request.method == "POST" and form.validate():
		password=form.password.data
		
		users=session['userName']
		cur= mysql.connection.cursor()
	
		cur.execute("UPDATE users SET password=%s WHERE userName=%s",(password,users))

		mysql.connection.commit()

		flash('Updated personal info','success')
		return redirect(url_for('homepage'))
		cur.close()
	return render_template('edit_password.html',form=form)


@app.route('/profile/address',methods=["POST","GET"])
@is_userlogged_in
def edit_address():
	form = addressForm(request.form)
	if request.method == "POST" and form.validate():
		
		address=form.address.data
		users=session['userName']
		cur= mysql.connection.cursor()


		cur.execute("UPDATE users SET address=%s WHERE userName=%s",(address,users))

		mysql.connection.commit()

		flash('Updated personal info','success')
		return redirect(url_for('homepage'))
		cur.close()
	return render_template('edit_address.html',form=form)


@app.route('/menu/add',methods=["POST","GET"])
@is_stafflogged_in
def add():
	form=addForm(request.form)
	if request.method=="POST" and form.validate():
		dishName=form.dishName.data
		price=form.price.data
		
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO menu (dishName,price) VALUES (%s,%s)",(dishName,price))
		mysql.connection.commit()
		cur.close()
		flash("added into the database","success")
		return redirect(url_for('menu'))
	return render_template("add.html",form=form)



@app.route('/menu/delete',methods=["POST","GET"])
@is_stafflogged_in
def delete():
	if request.method=="POST":
		dishID=request.form['dishID']

		cur = mysql.connection.cursor()

		cur.execute("DELETE FROM menu WHERE dishID =%s",(dishID))
		mysql.connection.commit()
		cur.close()
		flash("deleted from the database","success")
	return render_template("delete.html")
	

@app.route("/login",methods=["POST","GET"])
def login():
	
	if request.method=="POST":
		userName=request.form['userName']
		pwd=request.form['password']

		cur=mysql.connection.cursor()

		result = cur.execute("SELECT * FROM users WHERE userName=%s",[userName])
		if result >0:
			data=cur.fetchone()
			password=data['password']

			if pwd == password:
				session['logged_in']=True
				session['userName']=userName

				flash('Welcome ','success')
				return	render_template('homepage.html')
			else:
				error='invalid login'
				return render_template('login.html', error=error)
				cur.close()
		else:
			error="No such user"
			return render_template('login.html',error=error)
			
	return render_template("login.html")


@app.route("/login/staff", methods=["POST","GET"])
def stafflogin():
	if request.method=="POST":
		staffName=request.form['staffName']
		pwd=request.form['password']

		cur=mysql.connection.cursor()

		result = cur.execute("SELECT * FROM staffs WHERE staffName=%s",[staffName])
		if result >0:
			data=cur.fetchone()
			password=data['password']

			if pwd == password:
				session['logged_in']=True
				session['staffName']=staffName

				flash('Welcome staff','success')
				return	redirect(url_for('homepage'))
			else:
				error='invalid login'
				return render_template('stafflogin.html', error=error)
				cur.close()
		else:
			error="No such staff"
			return render_template('stafflogin.html',error=error)
			
	return render_template("stafflogin.html")

@app.route("/register", methods=['POST','GET'])
def register():
	form= RegisterForm(request.form)
	if request.method == "POST" and form.validate():

		userName=form.userName.data
		email=form.email.data
		address=form.address.data
		password=form.password.data
		
		cur = mysql.connection.cursor()

		cur.execute("INSERT INTO users (userName , email ,address , password) VALUES (%s , %s , %s , %s)",(userName,email,address,password))

		mysql.connection.commit()

		cur.close()

		flash('You can now login in login page','success')
		
		return redirect(url_for('login'))
	
	return render_template("register.html",form = form)
	

@app.route('/logout')
def logout():
	session.pop('userName',None)
	session.pop('staffName',None)
	flash('You are now logged out','success')
	return render_template('logout.html')


if __name__ == '__main__':
	app.run(debug=True)

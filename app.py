from flask import Flask, render_template, request, redirect, url_for, flash, g, session
import pymysql
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key=os.urandom(23564)

@app.before_request
def before_request():
	g.user=None
	if 'user' in session:
		g.user = session['user']

globalresult=[]

connection=pymysql.connect(host='localhost', user="root", password="", db="webapp1", charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/signup')
def sign():
	 return render_template('signup.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
   
	cursor = connection.cursor()     
	
	if request.method == 'POST':
		user = request.form
		name = user['name']
		username=user['username']
		emailid = user['emailid']
		password = user['password']

		try:
			query="INSERT INTO Users (name, username, emailid, password) VALUES (%s, %s, %s, %s)"
			cursor.execute(query,(name, username, emailid, password))
			connection.commit() 
   
		except:
			return render_template('alert.html')

		connection.close()    
		return redirect(url_for('login'))

@app.route('/login')
def log():
	session.pop('user', None)
	return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error=None
	session.pop('user', None)
	if request.method == 'POST':
		session.pop('user', None)
		user_input = request.form['username']
		password_input = request.form['password']
		cursor = connection.cursor() 
		cursor.execute("SELECT password FROM Users WHERE username=%s", user_input)
		myresult=cursor.fetchone()
		if myresult==None:
			error = 'Invalid username or password. Please try again!'
			flash("Invalid username or password")
			
		elif myresult['password']==password_input :
			session['user']=user_input
			return redirect(url_for('homequery'))
		else :
			error = 'Invalid username or password. Please try again!'
			return render_template('login.html', error = error)		

@app.route ('/')	
def homequery():
	if g.user:
		resultcab=[]
		resultbuy=[]
		cursor=connection.cursor()
		cursor.execute('SELECT * from Users where username=%s ',g.user)
		userid=cursor.fetchone()
		userid=userid['userid']
		cursor.execute("SELECT * from notifications where userid=%s and cabid!='0'",userid)
		resultcab1=cursor.fetchall()
		cursor.execute("SELECT * from notifications where userid=%s and sellid!='0'",userid)
		resultbuy1=cursor.fetchall()
		if resultcab1:
			for i in resultcab1 :
				resultcab.append(i)
		if resultbuy1:
			for i in resultbuy1 :
				resultbuy.append(i)		
				
			if resultcab==[] and resultbuy :
				cab='no notifications for cab sharing'
				buy='sell notifications'
				return render_template('home.html', resultbuy=resultbuy,cab=cab,buy=buy)
			if resultbuy==[] and resultcab:
				cab='cab notifications'
				buy='no notifications for products'
				return render_template('home.html', buy=buy,resultcab=resultcab,cab=cab)
			if resultbuy and resultcab :
				cab='cab notifications'
				buy='sell notifications'
				return render_template('home.html',resultbuy=resultbuy,resultcab=resultcab,cab=cab,buy=buy)
		else:	
			buy='no notifications for products'
			cab='no notifications for cab sharing'
			return render_template('home.html',buy=buy,cab=cab)
	return redirect(url_for('login'))	

@app.route('/buy', methods=['GET','POST'])
def buy():
	if g.user==None:
		return redirect(url_for('login'))	

	cursor=connection.cursor()
	result=[]
	print(result)
	cursor.execute('SELECT * FROM Users Where username=%s',g.user)
	user=cursor.fetchone()
	cursor.execute('SELECT * FROM sell where userid !=%s ORDER BY fare',user['userid'])
	x=cursor.fetchall()
	print(x)

	if request.method=='POST' :
			details=request.form
			sellid=details['key']
			print(sellid)
			cursor.execute('SELECT * FROM sell where sellid=%s',sellid)
			details=cursor.fetchone()
			ownerid=details['userid']
			cursor.execute('SELECT * FROM Users where userid=%s',ownerid)
			owner=cursor.fetchone()
			cursor.execute("INSERT INTO notifications(userid,sellid,buyid,productname,price,buy_name,buy_contact) VALUES (%s,%s,%s,%s,%s,%s,%s)",(owner['userid'],sellid,user['userid'],details['productname'],details['fare'],user['name'],user['contact']))
			connection.commit()
			return render_template('successbuy.html',owner=owner,details=details)	
	for i in x :
		result.append(i)
	print(result)
	if result:
		print(result)
		return render_template('index.html', result=result)
	else :
		return render_template('home.html')			


@app.route('/furniture', methods=['GET','POST'])
def furniture():
	if g.user==None:
		return redirect(url_for('login'))	

	cursor=connection.cursor()
	result=[]
	print(result)
	cursor.execute('SELECT * FROM Users Where username=%s',g.user)
	user=cursor.fetchone()
	cursor.execute("SELECT * FROM sell where userid !=%s and category='Furniture' ORDER BY fare",user['userid'])
	x=cursor.fetchall()
	print(x)

	if request.method=='POST' :
			details=request.form
			sellid=details['key']
			print(sellid)
			cursor.execute('SELECT * FROM sell where sellid=%s',sellid)
			details=cursor.fetchone()
			ownerid=details['userid']
			cursor.execute('SELECT * FROM Users where userid=%s',ownerid)
			owner=cursor.fetchone()
			cursor.execute("INSERT INTO notifications(userid,sellid,buyid,productname,price,buy_name,buy_contact) VALUES (%s,%s,%s,%s,%s,%s,%s)",(owner['userid'],sellid,user['userid'],details['productname'],details['fare'],user['name'],user['contact']))
			connection.commit()
			return render_template('successbuy.html',owner=owner,details=details)	
	for i in x :
		result.append(i)
	print(result)
	if result:
		print(result)
		return render_template('index.html', result=result)
	else :
		return render_template('home.html')	

@app.route('/crockery', methods=['GET','POST'])
def crockery():
	if g.user==None:
		return redirect(url_for('login'))	

	cursor=connection.cursor()
	result=[]
	print(result)
	cursor.execute('SELECT * FROM Users Where username=%s',g.user)
	user=cursor.fetchone()
	cursor.execute("SELECT * FROM sell where userid !=%s and category='Crockery' ORDER BY fare",user['userid'])
	x=cursor.fetchall()
	print(x)

	if request.method=='POST' :
			details=request.form
			sellid=details['key']
			print(sellid)
			cursor.execute('SELECT * FROM sell where sellid=%s',sellid)
			details=cursor.fetchone()
			ownerid=details['userid']
			cursor.execute('SELECT * FROM Users where userid=%s',ownerid)
			owner=cursor.fetchone()
			cursor.execute("INSERT INTO notifications(userid,sellid,buyid,productname,price,buy_name,buy_contact) VALUES (%s,%s,%s,%s,%s,%s,%s)",(owner['userid'],sellid,user['userid'],details['productname'],details['fare'],user['name'],user['contact']))
			connection.commit()
			return render_template('successbuy.html',owner=owner,details=details)	
	for i in x :
		result.append(i)
	print(result)
	if result:
		print(result)
		return render_template('index.html', result=result)
	else :
		return render_template('home.html')	

@app.route('/books', methods=['GET','POST'])
def books():
	if g.user==None:
		return redirect(url_for('login'))	

	cursor=connection.cursor()
	result=[]
	print(result)
	cursor.execute('SELECT * FROM Users Where username=%s',g.user)
	user=cursor.fetchone()
	cursor.execute("SELECT * FROM sell where userid !=%s and category='Books' ORDER BY fare",user['userid'])
	x=cursor.fetchall()
	print(x)

	if request.method=='POST' :
			details=request.form
			sellid=details['key']
			print(sellid)
			cursor.execute('SELECT * FROM sell where sellid=%s',sellid)
			details=cursor.fetchone()
			ownerid=details['userid']
			cursor.execute('SELECT * FROM Users where userid=%s',ownerid)
			owner=cursor.fetchone()
			cursor.execute("INSERT INTO notifications(userid,sellid,buyid,productname,price,buy_name,buy_contact) VALUES (%s,%s,%s,%s,%s,%s,%s)",(owner['userid'],sellid,user['userid'],details['productname'],details['fare'],user['name'],user['contact']))
			connection.commit()
			return render_template('successbuy.html',owner=owner,details=details)	
	for i in x :
		result.append(i)
	print(result)
	if result:
		print(result)
		return render_template('index.html', result=result)
	else :
		return render_template('home.html')

@app.route('/electronics', methods=['GET','POST'])
def electronics():
	if g.user==None:
		return redirect(url_for('login'))	

	cursor=connection.cursor()
	result=[]
	print(result)
	cursor.execute('SELECT * FROM Users Where username=%s',g.user)
	user=cursor.fetchone()
	cursor.execute("SELECT * FROM sell where userid !=%s and category='Electronics' ORDER BY fare",user['userid'])
	x=cursor.fetchall()
	print(x)

	if request.method=='POST' :
			details=request.form
			sellid=details['key']
			print(sellid)
			cursor.execute('SELECT * FROM sell where sellid=%s',sellid)
			details=cursor.fetchone()
			ownerid=details['userid']
			cursor.execute('SELECT * FROM Users where userid=%s',ownerid)
			owner=cursor.fetchone()
			cursor.execute("INSERT INTO notifications(userid,sellid,buyid,productname,price,buy_name,buy_contact) VALUES (%s,%s,%s,%s,%s,%s,%s)",(owner['userid'],sellid,user['userid'],details['productname'],details['fare'],user['name'],user['contact']))
			connection.commit()
			return render_template('successbuy.html',owner=owner,details=details)	
	for i in x :
		result.append(i)
	print(result)
	if result:
		print(result)
		return render_template('index.html', result=result)
	else :
		return render_template('home.html')		



@app.route('/sell')
def sellquery():
	if g.user:
		return render_template('sell.html')
	return redirect(url_for('login'))
@app.route('/sell', methods=['GET','POST'])
def sell():
	cursor = connection.cursor() 
	error=None    
	
	if request.method == 'POST':
		details = request.form
		category=details['category']
		fare=details['fare']
		productname=details['productname']
		file = request.files['image']

	
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		f = os.path.join(app.config['UPLOAD_FOLDER'], filename)

		cursor.execute('SELECT * from sell where image=%s',f)
		x=cursor.fetchone()
		
		while x!=None :
			f = os.path.join(app.config['UPLOAD_FOLDER'], 'i'+filename)
			cursor.execute('SELECT * from sell where image=%s',f)
			x=cursor.fetchone()
		

		file.save(f)
	else:
		error="Upload image file"
		return render_template('sell.html', error=error)	

	cursor.execute('SELECT * FROM Users Where username=%s',g.user)
	useridsell=cursor.fetchone()
	useridsell=useridsell['userid']


	if category=='0':
		error="Enter valid category of product"
		return render_template("sell.html", error = error)
	else :	
		cursor.execute("Insert INTO sell (category, fare, image, userid,productname) VALUES (%s, %s, %s, %s,%s)",(category,fare,f,useridsell,productname))
		connection.commit()
		return 'You will be notified if someone is willng to buy your product'
		
@app.route('/cab')
def cabquery():
	error=None
	if g.user:
		return render_template('cab.html')
	return redirect(url_for('login'))

@app.route('/cab', methods=['GET','POST'])
def cab():

	cursor = connection.cursor()
	if request.method =='POST':
		details=request.form
		date=details['date']
		time=details['time']
		source=details['Source']
		destination=details['Destination']

		if globalresult :
			del globalresult[:]
		cursor.execute("SELECT * FROM cab WHERE date=%s ORDER by time",date)
		x=cursor.fetchall()
		for i in x:
			if(i['source']==source):
				if(i['destination']==destination):
					if(i['NAS']!='0'):
						globalresult.append(i)
			
		if globalresult :
			return redirect(url_for('displaycheck'))
		else :
			flash('No cabs found..Please register for a cab')
			return redirect(url_for('cabregister'))

@app.route('/display')
def displaycheck() :
	error=None
	if g.user:
		return render_template('display.html', globalresult=globalresult)
	return redirect(url_for('login')) 

@app.route('/display', methods=['GET','POST'])
def success():
		
	cursor=connection.cursor()
	if request.method=='POST' :
		i=request.form
		if i:
			i=i['key']
			cursor.execute('SELECT * from Users where username=%s',g.user)
			owner=cursor.fetchone()
			owner=owner['userid']
			cursor.execute('SELECT * FROM cab Where cab_id=%s ',i)
			details=cursor.fetchone()
			x=details['userid']
			NAS=details['NAS']
			NAS-=1
			cursor.execute('UPDATE cab SET NAS=%s where cab_id=%s'%(NAS,i))
			connection.commit()
			cursor.execute('SELECT * from Users where userid=%s',x)
			userdetails=cursor.fetchone()
			cursor.execute("INSERT INTO notifications (userid,cabid,cabshareid,fare,source,destination,cab_name,cab_contact,date,time,NAS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(x,i,owner,details['fare'],details['source'],details['destination'],g.user,userdetails['contact'],details['date'],details['time'],details['NAS']))
			connection.commit()
			x=userdetails
			return render_template('success.html',x=x,details=details)	
		else: 
			return redirect(url_for('homequery'))	
	return render_template('display.html',globalresult=globalresult)		

@app.route('/cabregister')
def cabregisterquery():
	error=None
	if g.user:
		return render_template('cabregister.html')
	return redirect(url_for('login'))	

@app.route('/cabregister', methods=['GET','POST'])
def cabregister():
	
	cursor = connection.cursor() 
	error=None    
	
	if request.method == 'POST':
		details = request.form
		date=details['date']
		time=details['time']
		source=details['Source']
		destination=details['Destination']
		fare=details['fare']
		NAS=details['NAS']

		cursor.execute('SELECT * FROM Users Where username=%s',g.user)
		useridcab=cursor.fetchone()
		useridcab=useridcab['userid']
		if source!=destination and NAS!=0 and time!='9999':
			if source=='0' or destination=='0' :
				error="Enter valid source or destination"
				return render_template("cabregister.html", error = error)
			else :	
				cursor.execute("Insert INTO cab (date, time, source, destination, userid, fare, NAS,cab_name) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)",(date, time, source, destination, useridcab, fare, NAS,g.user))
				connection.commit()
				return 'You will be notified if someone is willng to share a cab with you'
		else :
			error="Enter valid details"
			return render_template("cabregister.html", error = error)	


	

@app.route ('/dropsession')
def dropsession():
	session.pop('user', None)
	return redirect(url_for('login'))


if __name__ == "__main__":
	app.run(debug=True)


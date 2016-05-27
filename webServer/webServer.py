#!python2

'''This is where all the normal webserver stuff goes. The OAuth flow is in oauth.py.'''

import logging
from datetime import datetime, timedelta
from urlparse import urlparse, urljoin

import os
from flask import Flask, session, request, render_template, redirect, url_for, g, flash
from itsdangerous import URLSafeTimedSerializer

from shared.models import Client, AuthCode, Token, User, Request
from forms import registerForm
from shared.sharedFuncs import login_required, lookupByUsername
from config import BaseConfig
from api.api_functions import verifyUser, FunctionReturn

app = Flask(__name__, template_folder='web_templates')
app.config.from_object(BaseConfig)

from email import sendConfirmEmail
from oauth import oauth

@app.before_request
def before_request():
	if 'username' in session:
		username = session['username']
		g.user = lookupByUsername(username)
	else:
		g.user = None

####### VIEWS #######

app.register_blueprint(oauth)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/tlogin', methods=('GET', 'POST'))
def touchLogin():
	#call user authorization and all that stuff
	if request.form.get("username"):
		user = lookupByUsername(username)
		if user:
			requestInDB = Request.query(Request.username == username).get()
			if not request:
				verifyUser(request.form.get("username"), "Touch Login")
				return FunctionReturn("Pending.", 6)
			elif requestInDB.resolved == -1:
				return FunctionReturn("Authentication Request Timed Out",  4)
			elif requestInDB.resolved == 0:
				return FunctionReturn("Pending.", 6)
			elif requestInDB.resolved == 1:
				session["username"]=username
				return FunctionReturn("Authenticated",  0)
		else:
			return FunctionReturn("User does not exist",  1)
	else:
		return FunctionReturn("Username is not there.", 5)

@app.route('/login', methods=('GET', 'POST'))
def login():
	next = request.args.get("next")
	if request.method == 'POST':
		username, password = request.form.get('username'), request.form.get('password')	#YES I KNOW WE'LL SWITCH TO HASHES AT SOME POINT
		next = request.form.get("next")	#if referred from oauth flow
		if validateUser(username, password):
			session['username'] = username
			if next and validateRedirect(next):
				return redirect(next)
			else:
				return redirect(url_for("home"))
		else:
			flash("Invalid credentials")
			return redirect(url_for("login"))

	return render_template('login.html', next = next)

@app.route("/register/", methods = ("GET", "POST"))
def register():
	form = registerForm()
	if g.user: 
		return redirect(url_for("profile"))
	if form.validate_on_submit():
		user = User(
			email = form.email.data,
			firstName = form.firstName.data,
			lastName = form.lastName.data,
			# password = form.password.data,
			birthday = datetime.strptime(form.birthday_month.data + '%02d'%form.birthday_day.data + form.birthday_year.data, "%b%d%Y").date(),
			username = form.username.data
		)
		logging.warning(str(user))
		sendConfirmEmail(user.email)

		user.put()
		session["username"] = user.username

		if not os.environ['SERVER_SOFTWARE'].startswith('Development'):	#if production, cuz mail doesn't work on dev.
			flash("A confirmation link has been sent to your email address.")
			return redirect(url_for("home"))
		else:
			token = URLSafeTimedSerializer(app.config['SECRET_KEY']).dumps(user.email, salt=app.config['SECURITY_PASSWORD_SALT'])
			confirm_url = url_for("confirmEmail", token = token, _external = True)
			return "<a href={0}>Confirm</a>".format(confirm_url)	#let developer do it manually

	return render_template("register.html", form = form)

@app.route("/confirm/<token>")
def confirmEmail(token):
	serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
	logging.warning(token)
	try:
		email = serializer.loads(
			token,
			salt=app.config["SECURITY_PASSWORD_SALT"],
			max_age=3600 # max age of confirmation token
		)
		user = User.query(User.email == email).get()
		if not user:
			flash("Confirmation link invalid.", "error")
			return redirect(url_for("home"))
		user.confirmed = True
		user.confirmedOn = datetime.now()
		user.put()
		flash('You have confirmed your account. Thanks!', 'success')
		return redirect(url_for("home"))
	except Exception as e:
		flash("Confirmation link expired.", "error")
		logging.warning(e)
		return redirect(url_for("home"))

@app.route("/resend/<userKey>")
@login_required
def resend(userKey):
	key = ndb.Key("User", userKey)
	user = key.get()
	if user:
		sendConfirmEmail(user.email)
	return redirect(url_for("home"))


@app.route("/profile")
@login_required
def profile():
	return "Not done yet"

@app.route("/logout")
def logout():
	session.clear()
	flash("You have been logged out", "success")
	return redirect(url_for("home"))

@app.errorhandler(404)
def page_not_found(e):
	"""Return a custom 404 error."""
	return 'Sorry, nothing at this URL.', 404

@app.errorhandler(500)
def application_error(e):
	"""Return a custom 500 error."""
	return 'Sorry, unexpected error: {}'.format(e), 500

@app.route("/_expire-authcode")
def expireAuthCode():
	if request.args.get("secret") == app.config["QUEUE_SECRET"]:
		code = request.args.get("code")
		codeInDB = AuthCode.query(AuthCode.code == code).get()
		if codeInDB:
			codeInDB.key.delete()
			return "Done", 200
		return "Code already deleted or did not exist", 200
	else:
		return "Unauthorized", 200

@app.route("/_expire-token")
def expireToken():
	if request.args.get("secret") == app.config["QUEUE_SECRET"]:
		access_token = request.args.get("access_token")
		tokenInDB = Token.query(Token.access_token == access_token).get()
		if tokenInDB:
			tokenInDB.key.delete()
			return "Done", 200
		return "Code already deleted or did not exist", 200
	else:
		return "Unauthorized", 503

##### LOGINS AND USERS #####

def validateUser(username, password):
	user = lookupByUsername(username)
	if not user:
		return False
	if user.password != password:
		logging.debug("Wrong password: " + user.password + "vs " + str(password))
		return False 
	return True

def validateRedirect(target):
	host_url = urlparse(request.host_url)
	redirect_url = urlparse(urljoin(request.host_url, target))
	return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc

#!python2

'''This is where all the normal webserver stuff goes. The OAuth flow is in oauth.py.'''

import logging
from datetime import datetime, timedelta
from urlparse import urlparse, urljoin
import os
import json

from flask import Flask, session, request, render_template, redirect, url_for, g, flash
from itsdangerous import URLSafeTimedSerializer
from google.appengine.ext import ndb

from shared.models import Client, AuthCode, Token, User, Request
from forms import clientRegisterForm
from shared.sharedFuncs import login_required, lookupByUsername, lookupClientByName
from config import BaseConfig
from api.api_functions import verifyUser, FunctionReturn

app = Flask(__name__, template_folder='web_templates')
app.config.from_object(BaseConfig)

from email import sendConfirmEmail
from oauth import oauth

####### VIEWS #######

app.register_blueprint(oauth)

@app.route('/')
def home():
	return render_template('home.html')

@app.route("/developers/")
def developerHome():
	return render_template("developerHome.html")

@app.route("/developers/clientRegister", methods=("GET", "POST"))
def devClientRegister():
	form = clientRegisterForm()
	if form.validate_on_submit():
		client = Client(
			name = form.clientName.data, #for convenience
			client_id = "",
			client_secret = "",
		#	scopes = ndb.StringProperty()
			redirect_url = "",
			email = form.email.data,
			password = form.password.data,
			confirmed = False
		)
		sendConfirmEmail(form.email.data)

		session["client"] = form.clientName.data;

		if not os.environ['SERVER_SOFTWARE'].startswith('Development'):	#if production, cuz mail doesn't work on dev.
			flash("Thanks for registering your client! A confirmation link has been sent to your email address.")
			return redirect(url_for("developerDashboard"))
		else:
			token = URLSafeTimedSerializer(app.config['SECRET_KEY']).dumps(user.key.urlsafe(), salt=app.config['SECURITY_PASSWORD_SALT'])
			confirm_url = url_for("confirmEmail", token = token, _external = True)
			return "<a href={0}>Confirm</a>".format(confirm_url)	#let developer do it manually

	return render_template("developerRegister.html", form = form)
	# return render_template("devClientRegister.html")

@app.route("/developers/dashboard/")
def developerDashboard():
	return "Placeholder"


# @app.route('/login/', methods=('GET','POST'))
# def login():
# 	clientId = request.args.get("clid") or "Touch Login"
# 	next = request.args.get("next")
# 	logging.debug(next)
# 	#call user authorization and all that stuff
# 	if request.method == 'POST':	#i.e. ajax call
# 		next = request.json.get("next")
# 		clientId = request.json.get("clid") or "Touch Login"
# 		if request.json.get("username"):
# 			user = lookupByUsername(request.json.get("username"))
# 			if user:
# 				statusRequest = verifyUser(user, clientId)
# 				if statusRequest.resolved == 1:	#SUCCESSFUL AUTH
# 					#logging.debug("4")
# 					session["username"]=user.username
# 					logging.debug(next)
# 					statusRequest.key.delete()
# 					if next and validateRedirect(next):
# 						logging.debug("redirecting to " + next)
# 						return json.dumps(vars(FunctionReturn(next,  0)))
# 					else:
# 						return json.dumps(vars(FunctionReturn(url_for("home"),  0)))
# 				elif statusRequest.resolved == -1:	#Timed out
# 					flash("Authentication request timed out. Please try again.", "error")
# 					statusRequest.key.delete()
# 					# logging.debug("2")
# 					return json.dumps(vars(FunctionReturn("Authentication request timed out. Please try again.",  4)))
# 				else:	#If this fires, shit has been messed up.
# 					logging.critical(request)
# 					return json.dumps(vars(FunctionReturn("No idea what happened.",  4)))	#Force reload on client-side
# 			else:
# 				# logging.debug("5")
# 				flash("User does not exist.", "error")
# 				return json.dumps(vars(FunctionReturn("User does not exist",  1)))
# 		else:
# 			# logging.debug("6")
# 			flash("Imma need a username, bruh.", "error")
# 			return json.dumps(FunctionReturn("Username is not there.", 5))
# 	else:
# 		# logging.debug("7")
# 		return render_template('login.html', next = next, clientId = clientId)

# # @app.route('/login', methods=('GET', 'POST'))
# # def login():
# # 	next = request.args.get("next")
# # 	if request.method == 'POST':
# # 		username, password = request.form.get('username'), request.form.get('password')	#YES I KNOW WE'LL SWITCH TO HASHES AT SOME POINT
# # 		next = request.form.get("next")	#if referred from oauth flow
# # 		if validateUser(username, password):
# # 			session['username'] = username
# # 			if next and validateRedirect(next):
# # 				return redirect(next)
# # 			else:
# # 				return redirect(url_for("home"))
# # 		else:
# # 			flash("Invalid credentials")
# # 			return redirect(url_for("login"))

# # 	return render_template('login.html', next = next)

# @app.route("/register/", methods = ("GET", "POST"))
# def register():
# 	form = registerForm()
# 	if g.user: 
# 		return redirect(url_for("profile"))
# 	if form.validate_on_submit():
# 		user = User(
# 			email = form.email.data,
# 			firstName = form.firstName.data,
# 			lastName = form.lastName.data,
# 			# password = form.password.data,
# 			birthday = datetime.strptime(form.birthday_month.data + '%02d'%form.birthday_day.data + form.birthday_year.data, "%b%d%Y").date(),
# 			username = form.username.data
# 		)
# 		#logging.warning(str(user))
# 		user.put()
# 		sendConfirmEmail(user)

# 		session["username"] = user.username

# 		if not os.environ['SERVER_SOFTWARE'].startswith('Development'):	#if production, cuz mail doesn't work on dev.
# 			flash("A confirmation link has been sent to your email address.")
# 			return redirect(url_for("home"))
# 		else:
# 			token = URLSafeTimedSerializer(app.config['SECRET_KEY']).dumps(user.key.urlsafe(), salt=app.config['SECURITY_PASSWORD_SALT'])
# 			confirm_url = url_for("confirmEmail", token = token, _external = True)
# 			return "<a href={0}>Confirm</a>".format(confirm_url)	#let developer do it manually

# 	return render_template("register.html", form = form)

# @app.route("/confirm/<token>")
# def confirmEmail(token):
# 	serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
# 	logging.warning(token)
# 	try:
# 		key = serializer.loads(
# 			token,
# 			salt=app.config["SECURITY_PASSWORD_SALT"],
# 			max_age=3600 # max age of confirmation token
# 		)
# 		user = ndb.Key(urlsafe=key).get()
# 		if not user:
# 			flash("Confirmation link invalid.", "error")
# 			return redirect(url_for("home"))
# 		user.confirmed = True
# 		user.confirmedOn = datetime.now()
# 		user.put()
# 		flash('You have confirmed your account. Thanks!', 'success')
# 		return redirect(url_for("home"))
# 	except Exception as e:
# 		flash("Confirmation link expired.", "error")
# 		logging.warning(e)
# 		return redirect(url_for("home"))

# @app.route("/resend/<userKey>")
# def resend(userKey):
# 	key = ndb.Key(urlsafe = userKey)
# 	user = key.get()
# 	logging.warning(user)
# 	if user:
# 		sendConfirmEmail(user)
# 	return redirect(url_for("home"))


# @app.route("/profile")
# @login_required
# def profile():
# 	return "Not done yet"

# @app.route("/logout")
# def logout():
# 	session.clear()
# 	flash("You have been logged out", "success")
# 	return redirect(url_for("home"))

# @app.errorhandler(404)
# def page_not_found(e):
# 	"""Return a custom 404 error."""
# 	return 'Sorry, nothing at this URL.', 404

# @app.errorhandler(500)
# def application_error(e):
# 	"""Return a custom 500 error."""
# 	return 'Sorry, unexpected error: {}'.format(e), 500

# @app.route("/_expire-authcode")
# def expireAuthCode():
# 	if request.args.get("secret") == app.config["QUEUE_SECRET"]:
# 		code = request.args.get("code")
# 		codeInDB = AuthCode.query(AuthCode.code == code).get()
# 		if codeInDB:
# 			codeInDB.key.delete()
# 			return "Done", 200
# 		return "Code already deleted or did not exist", 200
# 	else:
# 		return "Unauthorized", 200

# @app.route("/_expire-token")
# def expireToken():
# 	if request.args.get("secret") == app.config["QUEUE_SECRET"]:
# 		access_token = request.args.get("access_token")
# 		tokenInDB = Token.query(Token.access_token == access_token).get()
# 		if tokenInDB:
# 			tokenInDB.key.delete()
# 			return "Done", 200
# 		return "Code already deleted or did not exist", 200
# 	else:
# 		return "Unauthorized", 503

# ##### LOGINS AND USERS #####

# def validateUser(username, password):
# 	user = lookupByUsername(username)
# 	if not user:
# 		return False
# 	if user.password != password:
# 		logging.debug("Wrong password: " + user.password + "vs " + str(password))
# 		return False 
# 	return True

# def validateRedirect(target):
# 	host_url = urlparse(request.host_url)
# 	redirect_url = urlparse(urljoin(request.host_url, target))
# 	logging.critical(str(redirect_url))
# 	return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc

@app.template_filter('autoversion')	#so that js scripts don't cache
def autoversion_filter(filename):
	# determining fullpath might be project specific
	now = datetime.now()
	timestamp = str(now.minute) + str(now.second)
	newfilename = "{0}?v={1}".format(filename, timestamp)
	return newfilename
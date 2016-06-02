#!python2

from flask import Flask, render_template, request, url_for, redirect, session, flash
import requests
from werkzeug.serving import run_simple

app = Flask(__name__)
app.debug = True
client_id = "TestClient"
client_secret = "secret"
app.secret_key = "jiamjwolvma4io82u984um9mua9ufm98q2u298"
AUTH_SERVER_ROOT = "http://touch-login.appspot.com/"

@app.route('/')
def home():
	print(session.get('user'))
	return render_template("home.html", id = client_id, user = session.get("user"))

@app.route("/tl/redirect/")
def redirectFunc():
	code = request.args.get("code")
	tokenRequest = {'client_id': client_id, "client_secret": client_secret, "code": code}
	res = requests.post(AUTH_SERVER_ROOT + '/oauth/getToken', data=tokenRequest)
	res = dict(res.json())
	if res and (res.get("error") is None): 
		accessToken = res.get("access_token")
		dataRequest = {"client_id": client_id, "client_secret": client_secret, "access_token": accessToken}
		userData = requests.get(AUTH_SERVER_ROOT + "/oauth/getUserData", params = dataRequest)
		userData = dict(userData.json())
		session["user"] = userData
		print(session.get("user"))
		return redirect(url_for('home'))
	else:
		return res.get("error") or str(res)

@app.route("/logout")
def logout():
	session.clear()
	flash("You have been logged out", "success")
	return redirect(url_for("home"))

@app.route("/continue")
def example_continue():
	return render_template("example_continue.html")
	
# if __name__ == '__main__':
# 	run_simple('localhost', 5000, app,
# 			   use_reloader=True, use_debugger=True, use_evalex=True)
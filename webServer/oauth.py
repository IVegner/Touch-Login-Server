from flask import Blueprint, render_template, request, url_for, g, redirect, jsonify
from shared.models import Client, AuthCode, Token
import logging
from shared.sharedFuncs import login_required, randomString
from datetime import datetime, timedelta
from google.appengine.ext import ndb
from google.appengine.api import taskqueue
import time

oauth = Blueprint("oauth", __name__, template_folder = 'web_templates')

from webServer import app

@oauth.route("/oauth/authorize")
@login_required
def authorize():
	#logging.warning("AUTHORIZE THE USER IS " + str(g.user.username))

	if request.method == "GET":
		client_id = request.args.get("id")
		#logging.warning("Client id: " + client_id)
		if client_id and lookupClientByID(client_id) is not None:
			client = lookupClientByID(client_id)	#yes, yes, I know, I'm looking it up twice.
			return render_template("authorize.html", client = client)
		else:
			return "Bad request."

@oauth.route("/oauth/getcode", methods = ("GET", "POST"))
@login_required
def getAuthCode():
	#logging.warning("GETCODE THE USER IS " + str(g.user.username))
	code = randomString(32)
	client = lookupClientByID(request.form.get("client_id"))
	if client and request.form.get("confirm_yes"):
		redirectUrl = client.redirect_url
		codeDB = AuthCode(client_id = client.client_id, client = client.key, 
						  user = g.user.key, code = code, expires = datetime.now() + timedelta(seconds=app.config["AUTHCODE_EXPIRATION"]))
		codeDB.put()
		taskqueue.add(url='/_expire-authcode', params={'code': code, "secret": app.config["QUEUE_SECRET"]}, method="GET", countdown = app.config["AUTHCODE_EXPIRATION"])
		return redirect("{0}?code={1}&expires={2}".format(redirectUrl, code, app.config["AUTHCODE_EXPIRATION"]))
	else:
		logging.warning("DID NOT CONFIRM")
		return "<script>window.close()</script>"

@oauth.route("/oauth/getToken", methods = ("GET", "POST"))
def getToken():		#client does this
	client = lookupClientByID(request.form.get("client_id"))
	#logging.warning("CLIENT ID: " + str(request.form.get("client_id")))
	if client and client.client_secret == request.form.get("client_secret"):
		time.sleep(0.1)
		codeInDB = AuthCode.query(AuthCode.code == request.form.get("code")).get()
		#logging.warning("CODE IN DB:" + str(codeInDB))
		if codeInDB:
			tokenGrant = Token(client = client.key, user = codeInDB.user, access_token = randomString(32),
							   refresh_token = randomString(32), expires = datetime.now() + timedelta(seconds=app.config["ACCESSTOKEN_EXPIRATION"]))
			ndb.delete_multi(Token.query(Token.client == client.key and Token.user == codeInDB.user).fetch(keys_only = True)) #delete prior tokens
			tokenGrant.put()
			codeInDB.key.delete()
			taskqueue.add(url='/_expire-token', params={'access_token': tokenGrant.access_token, "secret": app.config["QUEUE_SECRET"]}, 
						  method="GET", countdown = app.config["ACCESSTOKEN_EXPIRATION"])
			return jsonify({"access_token": tokenGrant.access_token, 
							"refresh_token": tokenGrant.refresh_token, "expires": app.config["ACCESSTOKEN_EXPIRATION"]})
		else:
			return jsonify({"error": "Auth code expired or invalid"})
	return jsonify({"error": "Invalid credentials"})

@oauth.route("/oauth/getUserData")
def getUserData():
	client = lookupClientByID(request.args.get("client_id"))
	time.sleep(0.1)
	#tokenInDB = Token.query(ndb.AND(Token.access_token == request.args.get("access_token")), Token.client == client.key).get()
	tokenInDB = Token.query(Token.access_token == request.args.get("access_token")).get()
	#logging.warning(Token.query(Token.access_token == request.args.get("access_token")).get())
	if tokenInDB and request.args.get("client_secret") == client.client_secret:
		user = tokenInDB.user.get()
		logging.warning("USER FROM GETUSERDATA: " + str(user))
		return jsonify({"firstName": user.firstName, "username": user.username})
	else:
		return jsonify({"error": "Invalid token or credentials"})


def lookupClientByID(client_id):
	return Client.query(Client.client_id == client_id).get()

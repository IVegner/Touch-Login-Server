from functools import wraps
from flask import session, redirect, url_for, request, flash, g, Markup
import string
import random
from shared.models import User
import logging

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if session.get('username') is not None:
			#logging.debug("Debug of g.user: " + str(g.user))
			if g.user.confirmed == True:
				return f(*args, **kwargs)
			else:
				flash(Markup("Please confirm your email first. Didn\'t get the email? <a href=\"%s\">Resend</a>."
							 %url_for("resend", userKey = g.user.key.urlsafe())), "error")
				return redirect(url_for("home"))
		else:
			flash('Please log in first.', 'error')
			return redirect(url_for('login', next=request.url))
	return decorated_function

def randomString(size = 32):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

def lookupByUsername(username):
	user = User.query(User.username == username).get()
	if user is not None:
		return user
	else:
		return None
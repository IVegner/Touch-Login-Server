'''this shit works only on prod'''

from google.appengine.api import mail
from itsdangerous import URLSafeTimedSerializer
from webServer import app
from flask import url_for, render_template

def sendConfirmEmail(user):
	token = URLSafeTimedSerializer(app.config['SECRET_KEY']).dumps(user.key.urlsafe(), salt=app.config['SECURITY_PASSWORD_SALT'])
	confirm_url = url_for("confirmEmail", token = token, _external = True)
	html = render_template('_confirmEmail.html', confirm_url=confirm_url)
	subject = "Please confirm registration for TouchLogin"
	sendEmail(user.email, subject, html)

def sendEmail(email, subject, html):
	message = mail.EmailMessage(sender="TouchLogin.com Support <touchlogin@touch-login.appspotmail.com>",
                           		subject=subject)
	message.to = email
	message.html = html
	message.send()

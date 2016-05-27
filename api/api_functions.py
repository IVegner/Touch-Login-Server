#!python2

import logging
import time
import threading
from protorpc import messages, message_types, remote
import notifications
from shared.models import Request, User
from shared.sharedFuncs import lookupByUsername

authenticationRequestTimeout = 20
#####DATABASE INTERACTION ########

class FunctionReturn:	#to return messages and status codes to the API
	def __init__(self, message, code):
		self.returnMessage = message
		self.authStatusCode = code
   
def verifyUser(username, origin):
	user = lookupByUsername(username)
	if user is not None:
		timeout = 0
		token = user.APNsToken
		identifier = notifications.sendNotification(token, "{0} requests authentication".format(origin), authenticationRequestTimeout)
		Request(username = username, identifier = str(identifier), resolved = False).put()
		#notifications.sendNotification(token, "Identifier: {0}".format(identifier), authenticationRequestTimeout)	#temporary, lets tester know the identifier
		while(timeout < authenticationRequestTimeout):	#Wait for authentication, times out after preset time
			request = Request.query(Request.identifier == str(identifier)).get(use_cache=False, use_memcache=False)
			if request is not None and request.resolved == 1:
				return FunctionReturn("Authenticated",  0)
			else: 
				timeout += 0.5
				time.sleep(0.5)
		else: 
			request.resolved = -1
			request.put()
			return FunctionReturn("Authentication Request Timed Out",  4)

	else:
		return FunctionReturn("User does not exist",  1)

# def setAPNsTokenInDB(UID, token):
# 	user = _lookupByUID(UID)
# 	if user is not None:
# 		user.APNsToken = token
# 		user.put()
# 		return FunctionReturn("Successful",  0)
# 	else:
# 		return FunctionReturn("User does not exist",  1)

def authenticationConfirm(username, identifier, UID):
	logging.warning("AYY LMAO " + identifier + " " + UID)
	user = _lookupByUID(UID)
	if user is not None:	#check if user exists
		logging.warning("Hi")
		if user.username == username:	#check if given username matches the database entry
			request = Request.query(Request.identifier == str(identifier)).get()
			if request is not None:	#if the request exists
				logging.warning("Request found.")
				request.resolved = 1
				request.put()
				return FunctionReturn("Authenticated",  0)
			else:
				return FunctionReturn("Request was not found",  2)
		else: 
			return FunctionReturn("UID does not match username",  3)

	else: 
		logging.warning("Shit")
		return FunctionReturn("User does not exist",  1)

def _lookupByUID(UID):
	user = User.query(User.UID == UID).get()
	if user is not None:
		return user
	else:
		return None

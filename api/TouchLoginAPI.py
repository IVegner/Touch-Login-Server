import endpoints
from protorpc import messages, remote, message_types
import logging
from api_functions import *

########## Constants #######

package = "Touch Login"

######### API ##########

class AuthMessage(messages.Message):
	username = messages.StringField(1, required = True) #string param with ID 1
	origin = messages.StringField(2, required = True)

class setTokenHexMessage(messages.Message):
	UID = messages.StringField(1, required = True)		
	tokenHex = messages.StringField(2, required = True)

class AuthReplyMessage(messages.Message):
	username = messages.StringField(1, required = True)
	identifier = messages.StringField(2, required = True)
	UID = messages.StringField(3, required = True)

class ReturnMessage(messages.Message):
	returnMessage = messages.StringField(1)
	authStatusCode = messages.IntegerField(2)
	
@endpoints.api(name='touchloginAPI', version='v1')	#API declaration decorator
class TouchLoginAPI(remote.Service):

	INPUT_AUTH_RESOURCE = endpoints.ResourceContainer(AuthMessage)	#declares that the input will be an AuthMessage object
	INPUT_REGTOKEN_RESOURCE = endpoints.ResourceContainer(setTokenHexMessage)
	INPUT_AUTH_REPLY_RESOURCE = endpoints.ResourceContainer(AuthReplyMessage)
	 
	@endpoints.method(INPUT_AUTH_RESOURCE, ReturnMessage, path="AuthenticateUser",http_method='POST',name='AuthenticateUser')
	#INPUT_AUTH_RESOURCE is what the method expects in the request, ReturnMessage is the return, path is the url path to the method, 
	#http_method is the method (GET or POST) and the name is the name of the method in the API, which seems kinda redundant but is necessary

	def AuthenticateUser(self, request):	#Commented because this should be done internally
		status = verifyUser(request.username, request.origin)
		return ReturnMessage(returnMessage = status.returnMessage, authStatusCode = status.authStatusCode)

	# @endpoints.method(INPUT_REGTOKEN_RESOURCE, ReturnMessage, path="SetAPNsToken",http_method='POST',name='SetAPNsToken')
	# def SetAPNsToken(self, request):
	# 	status = setAPNsTokenInDB(request.UID, request.tokenHex)
	# 	return ReturnMessage(returnMessage = status.returnMessage, authStatusCode = status.authStatusCode)

	@endpoints.method(INPUT_AUTH_REPLY_RESOURCE, ReturnMessage, path="AuthenticationReply",http_method='POST',name='AuthenticationReply')
	def AuthenticationReply(self, request):
		status = authenticationConfirm(request.username, request.identifier, request.UID)
		return ReturnMessage(returnMessage = status.returnMessage, authStatusCode = status.authStatusCode)


APPLICATION = endpoints.api_server([TouchLoginAPI])




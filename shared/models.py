from google.appengine.ext import ndb

'''ndb models go here'''

class Request(ndb.Model):
	username = ndb.StringProperty()
	identifier = ndb.StringProperty()
	resolved = ndb.IntegerProperty(default = 0)
	addedOn = ndb.DateTimeProperty(auto_now_add=True)

class User(ndb.Model):	#database entity class with a bunch of properties
	UID = ndb.StringProperty()
	username = ndb.StringProperty()
	APNsToken = ndb.StringProperty()
	password = ndb.StringProperty(indexed = False, default = "test")
	email = ndb.StringProperty()
	firstName = ndb.StringProperty()
	lastName = ndb.StringProperty()
	birthday = ndb.DateProperty()
	registeredOn = ndb.DateTimeProperty(auto_now_add=True)
	admin = ndb.BooleanProperty(default=False)
	confirmed = ndb.BooleanProperty(default=False)
	confirmedOn = ndb.DateTimeProperty()

class Client(ndb.Model):			
	'''this is the permanent client record'''

	name = ndb.StringProperty()		#for convenience
	client_id = ndb.StringProperty()
	client_secret = ndb.StringProperty()
#	scopes = ndb.StringProperty()
	redirect_url = ndb.StringProperty()

class AuthCode(ndb.Model):		
	'''this is the temporary authorization token that is used to get an access token. Better to put in cache, but whatevs.'''

	client_id = ndb.StringProperty()
	client = ndb.KeyProperty(kind = Client)
	user = ndb.KeyProperty(kind = User)
	code = ndb.StringProperty()
	expires = ndb.DateTimeProperty()
#	scopes = ndb.StringProperty()

class Token(ndb.Model):
	'''This is the access token which is used for accessing the resource owner's stuff'''

	client = ndb.KeyProperty(kind = Client)
	user = ndb.KeyProperty(kind = User)
#	scopes = ndb.StringProperty()
	access_token = ndb.StringProperty()
	refresh_token = ndb.StringProperty()
	expires = ndb.DateTimeProperty()	
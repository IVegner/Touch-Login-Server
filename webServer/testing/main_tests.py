#!python2
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', "..", "libs"))
sys.path.append("C:\Program Files (x86)\Google\google_appengine")
sys.path.append("C:\Program Files (x86)\Google\google_appengine\lib\yaml\lib")

# I apologize for the above "code smells", I will eventually find the developers who made Google App Engine and kill them. I promise.
# Seriously though, no unittest support?!

from webServer.webServer import app as flask_app
from shared.models import User
import unittest

class ServerTestCase(unittest.TestCase):

	def setUp(self):
		os.environ['APPLICATION_ID'] = 'touch-login'
		datastore_file = '/dev/null'
		from google.appengine.api import apiproxy_stub_map,datastore_file_stub
		apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap() 
		stub = datastore_file_stub.DatastoreFileStub('touch-login', datastore_file)
		apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

		#If you think I know what that ^ does, you're wrong, I've got no idea.
		User(
			email = "ivanvegner@gmail.com",
			firstName = "Vanya",
			lastName = "Vegner",
			# password = form.password.data,
			username = "admin"
		).put()

		flask_app.config['TESTING'] = True
		self.app = flask_app.test_client()

	def tearDown(self):
		pass

	def testAppIsAlright(self):
		page = self.app.get("/")
		assert page.status_code == 200

	def testLogin(self):
		response = self.app.post('/login', data=dict(username="admin", password="test"), follow_redirects=True)
		print response.data
		assert 'Welcome, Vanya' in response.data

if __name__ == '__main__':
	unittest.main()

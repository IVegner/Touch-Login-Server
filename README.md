# Touch-Login -- Web Biometric Authentication

## What is TouchLogin?
TouchLogin is a web-based biometric authentication and account information transfer framework, which was a complete replacement for the ubiquitous "Login with Facebook/Google" OAuth buttons. The reason that a replacement was necessary was the inherent insecurity in using one password for every service -- if a malicious actor gets ahold of your Google password, not only is your Google account compromised, but so are all 3rd party accounts linked to it. TouchLogin utilized the iPhone's TouchID sensor instead of a password, so that users did not have to use one password for every service like they would if they had logged into multiple services with their Google/Facebook account, but instead could simply press their fingers to their TouchID sensors when it came time to login. Similar to Google/FB logins, TouchLogin removes the necessity to enter personal information manually when registering for a 3rd party account, due to its ability to populate the new account's user data from its own server.

Development suspended due to the simultaneous release of the same product by Auth0, and later Google and Microsoft as well. However, I am proud to note that this project was developed before the abovementioned companies.

## Features/Details
* Exact implementation of the OAuth2 protocol, meaning easy and maintainable integration with any websites that wished to use this service
* Very fast and efficient -- <1 second delay between server and app actions, convenient for the user
* Removes the user's necessity to enter in personal information such as name, email, etc. when registering -- he/she is able to set it up once in the TouchLogin profile and use it everywhere, similar to a Google/FB login.
* Hosted on Google App Engine, Python+Flask backend, raw Bootstrap front-end (I had yet to find out about the beauty of MVC), Swift iOS app (mostly not coded by me)

## Demo video 
https://www.youtube.com/watch?v=Db8qtwK__Qs

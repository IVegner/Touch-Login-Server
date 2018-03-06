# Touch-Login -- Web Biometric Authentication

## What is TouchLogin?
TouchLogin is a web-based biometric authentication framework, which was a complete replacement for the ubiquitous "Login with Facebook/Google" OAuth buttons. The reason that a replacement was necessary was the inherent insecurity in using one password for every service -- if a malicious actor gets ahold of your Google password, not only is your Google account compromised, but so are all 3rd party accounts linked to it. TouchLogin utilized the iPhone's TouchID sensor instead of a password, so that users did not have to use one password for every service like they would if they had logged into multiple services with their Google/Facebook account, but instead could simply press their fingers to their TouchID sensors when it came time to login. 

Development suspended due to the simultaneous release of the same product by Auth0, and later Google and Microsoft as well. However, I am proud to note that this project was developed before the abovementioned companies.

## Features/Details
* Exact implementation of the OAuth2 protocol, meaning easy and maintainable integration with any websites that wished to use this service
* Very fast and efficient -- <1 second delay between server and app actions, convenient for the user
* Hosted on Google App Engine, Python+Flask backend, raw Bootstrap front-end (I had yet to find out about the beauty of MVC), Swift iOS app (mostly not coded by me)

## Demo video 
https://www.youtube.com/watch?v=Db8qtwK__Qs

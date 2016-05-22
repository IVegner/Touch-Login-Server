from apns import APNs, Frame, Payload
import random
import logging

def sendNotification(token, message, timeout):
	apns = APNs(use_sandbox=False, cert_file='cert.pem', key_file='key.pem')
	frame = Frame()
	identifier = random.getrandbits(32)
	priority = 10
	payload = {"aps":{"alert": message, "sound":"default", "identifier":identifier}}
	#Payload(alert=message, sound="default", custom = {"identifier":identifier})
	frame.add_item(token, payload, identifier, timeout, priority)
	apns.gateway_server.send_notification_multiple(frame)
	return identifier

#there'll be more stuff here, I promise
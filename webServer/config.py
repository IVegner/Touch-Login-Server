class BaseConfig(object):
	"""Base configuration."""

	# main config
	SECRET_KEY = "Of90Pa0er<qo/EUA'xSIY2nnRcoj]2"
	SECURITY_PASSWORD_SALT = 'C576XcC7dtxvu3s4T1zxC71DwVAIRQERd'
	DEBUG = True
	WTF_CSRF_ENABLED = True
	DEBUG_TB_ENABLED = False
	DEBUG_TB_INTERCEPT_REDIRECTS = False

	QUEUE_SECRET = "afkadf00949mwafmkkvlpq09ra"
	AUTHCODE_EXPIRATION = 180 #2 minutes
	ACCESSTOKEN_EXPIRATION = 604800 #7 days
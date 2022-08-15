from os import getenv

REDIS_HOST = getenv('REDIS_HOST', 'redis')
REDIS_PORT = getenv('REDIS_PORT', '6379')

# redis db's
REDIS_BROKER = 0
REDIS_DEFAULT_CACHE = 1
REDIS_OTP_CACHE = 2
REDIS_UUID_CACHE = 3

OTP_EXPIRE_TIME = 180


# mail credentials
EMAIL_BACKEND = getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_USE_TLS = getenv('EMAIL_USE_TLS', True)
EMAIL_PORT = getenv('EMAIL_PORT', 587)
EMAIL_HOST_USER = getenv('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD', None)

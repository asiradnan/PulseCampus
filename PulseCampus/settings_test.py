from .settings import *

# Optional: Speed up tests by using faster password hashing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Optional: Disable email backend or use console backend
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
from .settings import *

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_ROOT = BASE_DIR / 'test_media'
# Optional: Speed up tests by using faster password hashing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Optional: Disable email backend or use console backend
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
from .base import *
import os
DEBUG = False


# ALLOWED_HOSTS = [
#     "yourdomain.com",
#     "www.yourdomain.com",
#     "api.yourdomain.com",
# ]
ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://yourdomain.com",
    "https://api.yourdomain.com",
    "http://localhost:5173",
    "https://rentoutindia.fawazmuhd06.workers.dev",
    
]

CORS_ALLOWED_ORIGINS = [
    "https://yourfrontend.vercel.app",
    "http://localhost:5173",
    "https://rentoutindia.fawazmuhd06.workers.dev",
]

CORS_ALLOW_CREDENTIALS = True

# -----------------------------
# SECURITY
# -----------------------------

SECURE_SSL_REDIRECT = False #change  wehn  vps iwht https 

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
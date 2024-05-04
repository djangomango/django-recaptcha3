DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.sqlite',
    }
}

INSTALLED_APPS = (
    'django_recaptcha3',
)

GOOGLE_RECAPTCHA_IS_ACTIVE = True
GOOGLE_RECAPTCHA_SECRET_KEY = 'your private key'
GOOGLE_RECAPTCHA_SITE_KEY = 'your public key'
GOOGLE_RECAPTCHA_DEFAULT_ACTION = 'generic'
GOOGLE_RECAPTCHA_SCORE_THRESHOLD = 0.5

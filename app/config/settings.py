
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import constants as messages
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

STATIC_URL = '/static/'

DEBUG = True

ALLOWED_HOSTS = ["*"]

SITE_ID = 1

CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'corsheaders',
    'compressor',
    'notifications',
    'sorl.thumbnail',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'tinymce',
    'mapbox_location_field',
    'phonenumber_field',
    'chartjs',
    'api',
    'club',
    'connection',
    'event',
    'public',
    'shop',
]
# sont utilisées pour le traitement des requêtes et des réponses HTTP.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/ 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#définit les validateurs de mot de passe utilisés pour vérifier la force et la complexité des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DATE_INPUT_FORMATS = ['%d/%m/%Y']
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French')),

]
LOCALE_PATHS = [BASE_DIR / 'locale']

STATIC_URL = '/static/'
MEDIA_URL = '/uploads/'
MEDIA_ROOT = BASE_DIR / 'uploads'

if DEBUG:
    STATICFILES_DIRS = [BASE_DIR, 'static']
else:
    STATIC_ROOT = BASE_DIR / 'static'


COMPRESS_ROOT = BASE_DIR / 'static'
COMPRESS_ENABLED = True
STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)


MESSAGE_TAGS = {
    messages.DEBUG: 'text-gray-700 bg-gray-100 border-gray-500 dark:bg-gray-200 absolute bottom-6 right-5 p-4 w-full max-w-xs rounded-lg shadow animate-bounce',
    messages.INFO: 'text-blue-700 bg-blue-100 border-blue-500 dark:bg-blue-200 absolute bottom-6 right-5 p-4 w-full max-w-xs rounded-lg shadow animate-bounce',
    messages.SUCCESS: 'text-green-700 bg-green-100 border-green-500 dark:bg-green-200 absolute bottom-6 right-5 p-4 w-full max-w-xs rounded-lg shadow animate-bounce',
    messages.WARNING: 'text-yellow-700 bg-yellow-100 border-yellow-500 dark:bg-yellow-200 absolute bottom-6 right-5 p-4 w-full max-w-xs rounded-lg shadow animate-bounce',
    messages.ERROR: 'text-red-700 bg-red-100 border-red-500 dark:bg-red-200 absolute bottom-6 right-5 p-4 w-full max-w-xs rounded-lg shadow animate-bounce',

}
LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_ON_GET = True
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 180

ACCOUNT_FORMS = {
    'login': 'connection.forms.CustomLoginForm',
    'signup': 'connection.forms.CustomSignupForm',
    'reset_password': 'connection.forms.CustomResetPasswordForm',
    'change_password': 'connection.forms.CustomPasswordChangeForm'
}
# l'application est en mode de développement if 
# if DEBUG:
#     EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#else:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)

MAPBOX_KEY = config('MAPBOX_KEY')
default_map_attrs = {  
 "style": "mapbox://styles/mapbox/streets-v12",
 "zoom": 5,
 "center": [5.15, 46.21],
 "cursor_style": 'pointer',
 "marker_color": "red",
 "rotate": False,
 "geocoder": True,
 "fullscreen_button": True,
 "navigation_buttons": True,
 "track_location_button": True, 
 "readonly": True,
 "placeholder": _("Pick a location on map below"), 
 "language": "auto",
 "message_404": _("undefined address"), 
 }
#editeur de text
TINYMCE_COMPRESSOR = False
TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 300,
    "skin": "oxide-dark",
    "content_css": "dark",
    "menubar": False,
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
}



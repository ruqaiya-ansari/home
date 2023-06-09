import os

 # noqa
from .settings import *  # noqa
from .settings import BASE_DIR
 


hostname = os.environ.get('HTTP_HOST', '')

# Add your custom domain(s) to the list of allowed hosts
ALLOWED_HOSTS = ['www.mysterycastel.com', 'mysterycastel.com']

# Add your custom domain(s) to the list of CSRF trusted origins
CSRF_TRUSTED_ORIGINS = ['https://www.mysterycastel.com', 'https://mysterycastel.com']

# Check if the hostname matches the default domain
if hostname and (hostname == 'classicreaders.azurewebsites.net' or hostname == 'www.classicreaders.azurewebsites.net'):
    # Add your default domain(s) to the list of allowed hosts
    ALLOWED_HOSTS += ['classicreaders.azurewebsites.net', 'www.classicreaders.azurewebsites.net']

    # Add your default domain(s) to the list of CSRF trusted origins
    CSRF_TRUSTED_ORIGINS += ['https://classicreaders.azurewebsites.net', 'https://www.classicreaders.azurewebsites.net']
DEBUG = False

# WhiteNoise configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DEFAULT_FILE_STORAGE = 'myclassic.azure_storage.AzureMediaStorage'
STATICFILES_STORAGE = 'myclassic.azure_storage.AzureStaticStorage'

AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = os.getenv('AZURE_ACCOUNT_KEY')
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'

STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'


CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_BASEPATH = f"https://{AZURE_CUSTOM_DOMAIN}/static/ckeditor/ckeditor/"



# Configure Postgres database based on connection string of the libpq Keyword/Value form
# https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': conn_str_params['dbname'],
        'HOST': conn_str_params['host'],
        'USER': conn_str_params['user'],
        'PASSWORD': conn_str_params['password'],
    }
}

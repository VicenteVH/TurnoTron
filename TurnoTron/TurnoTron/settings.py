from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Se define el directorio base del proyecto mediante el uso de la clase Path del módulo pathlib.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# Configuraciones rápidas para el desarrollo. Estas configuraciones no son adecuadas para producción.
# El DEBUG se establece en True para habilitar el modo de depuración.
# Se debe cambiar a False en entornos de producción.
DEBUG = True

SECRET_KEY = 'django-insecure-n2n*fl6c314w3=_y=i(_@%#lqin1)h*gcosu_q=#yab7dg3wep'
# Lista de hosts permitidos para el proyecto. Se deja vacío para permitir cualquier host.
ALLOWED_HOSTS = []


# Application definition
# Definición de las aplicaciones instaladas en el proyecto.

INSTALLED_APPS = [
    # Aplicaciones contribuidas por Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Aplicación personalizada del proyecto (crm)
    'crm',
]

# Middleware utilizado por el proyecto.
# El middleware es un framework de procesamiento de solicitudes y respuestas.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de la URL raíz para enrutar las solicitudes.
ROOT_URLCONF = 'TurnoTron.urls'

# Configuración de plantillas para el proyecto.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Configuración de la aplicación de servidor WSGI (Web Server Gateway Interface).
WSGI_APPLICATION = 'TurnoTron.wsgi.application'


# Database
# Configuración de la base de datos utilizada por el proyecto.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# Configuración de la validación de contraseñas para los usuarios.
# Se especifican varios validadores predefinidos proporcionados por Django.
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
# Configuración para admitir la internacionalización y la localización.
LANGUAGE_CODE = 'es-us'  # Código de idioma predeterminado.
TIME_ZONE = 'UTC'  # Zona horaria predeterminada.
USE_I18N = True  # Habilitar la internacionalización.
USE_TZ = True  # Habilitar el uso de zonas horarias.


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# Configuración del tipo de campo clave primaria predeterminado.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Campo de clave primaria predeterminado para los modelos.

# Modelo Usuario
AUTH_USER_MODEL = 'crm.User'
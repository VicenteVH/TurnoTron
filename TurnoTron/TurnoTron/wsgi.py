import os
from django.core.wsgi import get_wsgi_application

# Configurar la variable de entorno 'DJANGO_SETTINGS_MODULE' con el valor 'TurnoTron.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TurnoTron.settings')

# Obtener la aplicación WSGI de Django
application = get_wsgi_application()

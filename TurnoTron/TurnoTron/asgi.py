import os
from django.core.asgi import get_asgi_application

# Configurar la variable de entorno 'DJANGO_SETTINGS_MODULE' con el valor 'TurnoTron.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TurnoTron.settings')

# Obtener la aplicación ASGI de Django
application = get_asgi_application()


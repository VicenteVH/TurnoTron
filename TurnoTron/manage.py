#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

# Importación de módulos necesarios
import os
import sys

def main():
    """Run administrative tasks."""
    # Establecer la configuración de Django para el proyecto
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TurnoTron.settings')
    
    try:
        # Importar la función execute_from_command_line del módulo django.core.management
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Manejar la excepción si Django no se puede importar
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Ejecutar la función execute_from_command_line con los argumentos del script
    execute_from_command_line(sys.argv)

# Verificar si este archivo se está ejecutando como el programa principal
if __name__ == '__main__':
    # Llamar a la función main() si este archivo es el punto de entrada principal
    main()


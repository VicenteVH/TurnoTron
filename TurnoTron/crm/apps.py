from django.apps import AppConfig

class CrmConfig(AppConfig):  # Define una clase CrmConfig que hereda de AppConfig
    default_auto_field = 'django.db.models.BigAutoField'  # Configura el campo de clave primaria automática
    name = 'crm'  # Establece el nombre de la aplicación como 'crm'

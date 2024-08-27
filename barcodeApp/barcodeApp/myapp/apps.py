from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

# apps.py
# from django.apps import AppConfig

# class MyAppConfig(AppConfig):
#     name = 'myapp'

#     def ready(self):
#         import myapp.signals  # Ensure that the signals are connected
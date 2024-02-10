"""
WSGI config for cours project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Définit le module de configuration des paramètres Django pour le projet
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cours.settings.py')

# Récupère l'application WSGI pour le projet Django
application = get_wsgi_application()
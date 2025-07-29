"""
ASGI config for poll_sys project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

settings_module = 'poll_sys.deployment_settings' if os.environ.get('RENDER_EXTERNAL_HOSTNAME') else 'poll_sys.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poll_sys.settings')

application = get_asgi_application()

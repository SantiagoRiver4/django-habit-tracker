import os

from django.core.wsgi import get_wsgi_application

# Apunta a tu módulo de settings del proyecto
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# Vercel espera encontrar "app" como entrada WSGI
app = get_wsgi_application()

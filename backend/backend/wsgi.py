import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Production")

from configurations.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()

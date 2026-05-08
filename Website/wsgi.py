"""
WSGI config for Website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

try:
    import os
    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Website.settings')

    application = get_wsgi_application()
except ImportError as e:
    print(f"""\n Error: Required modules not available. {e}
     Please ensure Django is installed and settings are correct.\n""")
    application = None
except Exception as e:
    print(f"""\n Error: Failed to configure WSGI application. {e}
     Please ensure Django is installed and settings are correct.\n""")
    application = None
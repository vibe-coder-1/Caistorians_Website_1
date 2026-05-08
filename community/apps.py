try:
    from django.apps import AppConfig
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")

class CommunityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'community'

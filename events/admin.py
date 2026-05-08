try:
    from django.contrib import admin
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")
    
# Register your models here.

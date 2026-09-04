"""
URL configuration for Website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
try:
    from django.contrib import admin
    from django.urls import path, include
    from django.conf import settings
    from django.conf.urls.static import static
    from error_handling.views import custom_404_handler, custom_500_handler
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")
    urlpatterns = []
else:
    urlpatterns = [

        path('admin/', admin.site.urls),
        path('', include('Main.urls')),
        path('accounts/', include('Accounts.urls')),
        path('interactions/', include('interactions.urls', namespace='interactions')),
        path('events/', include('events.urls', namespace='events')),
        path('community/', include('community.urls', namespace='community')),
        path('custom_admin/', include('custom_admin.urls', namespace='custom_admin')),
        path('schools/', include('schools.urls', namespace='schools')),
        path('news/', include('news.urls', namespace='news')),
        path('notifications/', include('notifications.urls', namespace='notifications')),
        path('fundraisers/', include('fundraisers.urls', namespace='fundraisers')),
        path('chat/', include('chat.urls', namespace='chat')),
        path('error-handling/', include('error_handling.urls', namespace='error_handling')),
    ]

    handler404 = custom_404_handler
    handler500 = custom_500_handler

    # Serve media files in development only
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

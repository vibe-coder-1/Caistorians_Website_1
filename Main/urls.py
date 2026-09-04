try:
    from django.urls import path
    from . import views
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")

app_name = 'Main'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('site_home/', views.site_home, name='site_home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('history/', views.history, name='history'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_service/', views.terms_of_service, name='terms_of_service'),
]
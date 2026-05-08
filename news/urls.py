try:
    from django.urls import path
    from . import views
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")
app_name = 'news'
urlpatterns = [
    path('updates/', views.updates, name='updates'),
    path('create_update/', views.births_deaths_and_marriages, name='create_update'),
]
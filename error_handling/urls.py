from django.urls import path
from . import views

app_name = 'error_handling'

urlpatterns = [
    path('', views.error_handling_home, name='home'),
    path('<str:error_code>/', views.error_page, name='error_page'),
]

from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('redirect/', views.redirect_to_chat, name='chat_redirect'),  # /chat/
    path('<int:cohort_year>/', views.cohort_chat_view, name='cohort_chat'),  # /chat/2025/
]

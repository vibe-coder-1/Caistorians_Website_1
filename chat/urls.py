try:
    from django.urls import path
    from . import views
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")

app_name = "chat"

urlpatterns = [
    path('redirect/', views.redirect_to_chat, name='chat_redirect'),  # /chat/
    path('<int:cohort_year>/', views.cohort_chat_view, name='cohort_chat'),  # /chat/2025/
]

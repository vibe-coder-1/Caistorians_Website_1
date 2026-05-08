try:
    from django.urls import path
    from . import views
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")

app_name = "notifications"

urlpatterns = [
    path("", views.notifications_list, name="list"),
    path("read/<int:pk>/", views.mark_as_read, name="mark_as_read"),  # ✅ delete on read
]

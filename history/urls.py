# history/urls.py
from django.urls import path
from . import views

app_name = "history"

urlpatterns = [
    path("", views.history_page_views, name="event_list"),
]

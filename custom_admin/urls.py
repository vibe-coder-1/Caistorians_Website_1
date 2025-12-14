from django.urls import path
from . import views

app_name = "custom_admin"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    
    # Users
    path("user/<int:user_id>/delete/", views.delete_user, name="delete_user"),
    
    # Events
    path("approve-event/<int:event_id>/", views.approve_event, name="approve_event"),
    path("event/<int:event_id>/delete/", views.delete_event, name="delete_event"),
    
    # Photos
    path("photo/<int:photo_id>/approve/", views.approve_photo, name="approve_photo"),
    path("photo/<int:photo_id>/delete/", views.delete_photo, name="delete_photo"),
    
    # Stories
    path("story/<int:story_id>/approve/", views.approve_story, name="approve_story"),
    path("story/<int:story_id>/delete/", views.delete_story, name="delete_story"),

    # Reports
    path("report/<int:report_id>/resolve/", views.resolve_report, name="resolve_report"),


]

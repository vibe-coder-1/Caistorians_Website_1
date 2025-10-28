from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "community"
urlpatterns = [
    # Photos
    path("upload-photo/", views.upload_photo, name="upload_photo"),
    path("gallery/", views.gallery_view, name="gallery"),
    path("photo/<int:pk>/delete/", views.delete_photo, name="delete_photo"),
    # Stories
    path("submit-story/", views.submit_story, name="submit_story"),
    path("stories/", views.story_list, name="story_list"),
    path("stories/<int:pk>/", views.story_detail, name="story_detail"),
    path("stories/<int:pk>/delete/", views.delete_story, name="delete_story"),

] 
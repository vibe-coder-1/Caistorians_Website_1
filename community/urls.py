# # from django.urls import path
# # from . import views
# # from django.conf import settings
# # from django.conf.urls.static import static

# # app_name = "community"
# # urlpatterns = [
# #     # Photos
# #     path("upload-photo/", views.upload_photo, name="upload_photo"),
# #     path("gallery", views.gallery_view, name="gallery"),
# #     path("gallery/", views.gallery_photo_view, name="gallery_photo"),
# #     path("photo/<int:pk>/delete/", views.delete_photo, name="delete_photo"),
# #     # Stories
# #     path("submit-story/", views.submit_story, name="submit_story"),
# #     path("stories/", views.story_list, name="story_list"),
# #     path("stories/<int:pk>/", views.story_detail, name="story_detail"),
# #     path("stories/<int:pk>/delete/", views.delete_story, name="delete_story"),

# # ] 

# from django.urls import path
# from . import views
# from django.conf import settings
# from django.conf.urls.static import static

# app_name = "community"

# urlpatterns = [
#     # Photos
#     path("upload-photo/", views.upload_photo, name="upload_photo"),
#     path("gallery/", views.gallery_view, name="gallery"),
#     path("gallery/photo/", views.gallery_photo_view, name="gallery_photo"),
#     path("photo/<int:pk>/delete/", views.delete_photo, name="delete_photo"),

#     # Stories
#     path("submit-story/", views.submit_story, name="submit_story"),
#     path("stories/", views.story_list, name="story_list"),
#     path("stories/<int:story_id>/", views.story_detail, name="story_detail"),
#     path("stories/<int:pk>/delete/", views.delete_story, name="delete_story"),

#     # Stripe payment routes
#     path("stories/<int:story_id>/create-checkout-session/", views.create_story_checkout_session, name="create_story_checkout_session"),
#     path("stories/success/<int:story_id>/", views.story_success, name="story_success"),
#     path("stories/cancel/<int:story_id>/", views.story_cancel, name="story_cancel"),
#     path("stripe/webhook/", views.stripe_webhook, name="stripe_webhook"),
# ]

# # Serve media files in development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "community"


from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [

]


urlpatterns = [
    # Photos
    path("upload-photo/", views.upload_photo, name="upload_photo"),
    path("gallery/", views.gallery_view, name="gallery"),
    path("gallery/photo/", views.gallery_photo_view, name="gallery_photo"),
    path("photo/<int:pk>/delete/", views.delete_photo, name="delete_photo"),

    # Stories
    path("submit-story/", views.submit_story, name="submit_story"),
    path("stories/", views.story_list, name="story_list"),
    path("stories/<int:story_id>/", views.story_detail, name="story_detail"),
    path("stories/<int:pk>/delete/", views.delete_story, name="delete_story"),

    # Stripe payments
    path("stories/<int:story_id>/create-checkout-session/", views.create_story_checkout_session, name="create_story_checkout_session"),
    path("stories/success/<int:story_id>/", views.story_success, name="story_success"),
    path("stories/cancel/<int:story_id>/", views.story_cancel, name="story_cancel"),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

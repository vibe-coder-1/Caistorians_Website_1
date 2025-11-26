# fundraisers/urls.py
from django.urls import path
from . import views

app_name = "fundraisers"

urlpatterns = [
    path('list/', views.fundraiser_list, name='fundraiser_list'),
    path('create/', views.create_fundraiser, name='create_fundraiser'),
    path('<int:fundraiser_id>/', views.fundraiser_detail, name='fundraiser_detail'),
    path('<int:fundraiser_id>/checkout/', views.create_checkout_session, name='checkout'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('success/', views.success, name='fundraiser_success'),
    path('cancel/', views.cancel, name='fundraiser_cancel'),
    path('<int:story_id>/checkout/', views.create_story_checkout_session, name='create_story_checkout_session'),

]

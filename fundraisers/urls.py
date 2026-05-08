try:
    from django.urls import path
    from . import views
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")

app_name = "fundraisers"

urlpatterns = [
    # Fundraiser pages
    path('list/', views.fundraiser_list, name='fundraiser_list'),
    path('create/', views.create_fundraiser, name='create_fundraiser'),
    path('<int:fundraiser_id>/', views.fundraiser_detail, name='fundraiser_detail'),

    # Fundraiser checkout (creates Stripe session)
    path('<int:fundraiser_id>/checkout/', views.create_checkout_session, name='checkout'),

    # Stripe webhook (IMPORTANT)
    #path('webhook/', views.stripe_webhook, name='stripe_webhook'),

    # Success / cancel
    path('success/', views.success, name='fundraiser_success'),
    path('cancel/', views.cancel, name='fundraiser_cancel'),
]

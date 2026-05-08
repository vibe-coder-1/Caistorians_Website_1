try:
    from django.urls import path
    from . import views
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")

app_name = 'Accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='create_account'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path("profile/<str:username>/", views.public_profile_view, name="public_profile"),
    path("directory/", views.directory_view, name="directory"),
    path('privacy/', views.privacy, name='privacy'),
    path('download_data/', views.download_data, name='download_data'),
]
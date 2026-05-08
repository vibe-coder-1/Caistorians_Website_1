try:
    from django.urls import path
    from . import views
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")
    
app_name = 'schools'

urlpatterns = [
    path('create/', views.create_school_view, name='create_school'),
    path('school_list/', views.school_list_view, name='school_list'),
    path('<str:school_name>/', views.school_profile_view, name='school_profile'),  # <- updated
    path('<int:school_id>/edit/', views.edit_school_view, name='edit_school'),
]

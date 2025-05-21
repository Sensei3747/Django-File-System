from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_user_profile, name='create_profile'),
    path('edit/<int:pk>/', views.edit_user_profile, name='edit_profile'),
    path('profiles/', views.view_profiles, name='view_profiles'),
]

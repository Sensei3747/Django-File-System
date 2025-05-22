from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('users/', views.user_list_view, name='list_view'),
    path('chat/<int:receiver_id>/', views.chat_page, name='chat-page'),
]
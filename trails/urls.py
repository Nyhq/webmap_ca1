from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.trail_list, name='trail_list'),
    path('trail/<int:pk>/', views.trail_detail, name='trail_detail'),
    path('trail/<int:pk>/', views.trail_detail, name='trail_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='trail_list'), name='logout'),
    path('register/', views.register, name='register'),
]

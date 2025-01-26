from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('news/', views.news_home, name='news_home'),
    path('blogs/', views.blog_dashboard, name='blog_dashboard'),
    path('blogs/create/', views.create_blog, name='create_blog'),
    path('blogs/delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('api/admin/blogs/', views.admin_blog_api, name='admin_blog_api'),
]
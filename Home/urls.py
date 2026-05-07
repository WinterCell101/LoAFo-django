from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import logout_view

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.login_view, name='login'),
    path('report/', views.report_item, name='report_item'),
    path('search/', views.search_items, name='search_items'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
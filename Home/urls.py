from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('report/', views.report_item, name='report_item'),
    path('search/', views.search_items, name='search_items'),
]
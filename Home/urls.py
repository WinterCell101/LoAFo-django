from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('search/', views.search_items, name='search_items'),
    path('report/', views.report_item, name='report_item'),
    path('home/', views.home, name="home"),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password_view, name='reset_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

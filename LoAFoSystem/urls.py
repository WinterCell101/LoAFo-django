from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from Home import views  # Import the file where your home and signup_view live

urlpatterns = [
    path('admin/', admin.site.urls),

    # Social Auth (Google)
    path('social-auth/', include('social_django.urls', namespace='social')),

    # Root is Login (http://127.0.0.1:8000/)
    path('', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),

    # Standard Logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Signup - pointing to the function in Home/views.py
    path('register/', views.signup_view, name='signup'),
    path('search/', views.search_items, name='search_items'),
    path('report/', views.report_item, name='report_item'),
    # Dashboard/Home (Added a trailing slash for consistency)
    path('home/', views.home, name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
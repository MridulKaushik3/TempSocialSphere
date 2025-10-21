from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from tweet import views  # Correct import from tweet app

urlpatterns = [
    path('', views.home, name='home'),  # Home view from tweet app
    path('admin/', admin.site.urls),
    path('tweet/', include('tweet.urls')),  # App-level URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Django auth
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
